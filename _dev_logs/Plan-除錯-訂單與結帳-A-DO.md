# 除錯執行紀錄：確認付款並建立訂單

本文件記錄了「確認付款並建立訂單」功能的除錯過程。

## 1. 程式碼審查

- **審查對象**: `orders/views.py` 和 `orders/models.py`。
- **結論**:
    - `models.py` 結構清晰，無明顯問題。
    - `views.py` 中的 `create_order` 視圖存在兩個主要風險：
        1.  **缺乏資料庫交易**: 寫入資料庫的操作（建立 Order、建立 OrderItem、刪除 Cart）沒有原子性，中途失敗會導致資料不一致。
        2.  **未處理 `Cart.DoesNotExist`**: 如果使用者因異常流程進入該頁面而沒有購物車，`Cart.objects.get()` 會引發 500 錯誤。

## 2. 實施修正

- **目標**: 提升 `create_order` 視圖的穩定性與健壯性。
- **操作**:
    1.  **引入資料庫交易**:
        - 匯入 `from django.db import transaction`。
        - 使用 `with transaction.atomic():` 將 `create_order` 視圖中的所有資料庫寫入操作包裹起來。
    2.  **增加錯誤處理**:
        - 使用 `try...except Cart.DoesNotExist:` 結構來捕捉購物車不存在的錯誤，並將使用者安全地重導向回購物車頁面。
        - 增加了對空購物車的檢查。
    3.  **增加日誌記錄**:
        - 匯入 `logging` 模組。
        - 在 `create_order` 視圖的關鍵節點（開始、建立成功、清除購物車、發生例外）加入了詳細的日誌記錄 (`logger.info`, `logger.error`)。
    4.  **強化付款頁面**:
        - 同樣為 `payment_page` 視圖增加了對購物車不存在或為空的檢查，提高了健壯性。
- **結果**: `orders/views.py` 檔案已被更新，新的 `create_order` 視圖現在具備了資料庫交易的原子性、更完善的錯誤處理和日誌記錄功能。

---
**除錯與修正完成**
