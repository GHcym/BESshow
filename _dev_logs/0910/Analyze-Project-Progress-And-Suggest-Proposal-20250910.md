# BESSOW 專案後續開發與完善建議書

**日期:** 2025年09月10日
**提案人:** Gemini AI

## 1. 前言

本建議書基於對 BESSOW 專案的全面分析，旨在提供一系列具體、可執行的後續開發與改善方案。核心目標是**提升系統安全性**、**優化開發與維護流程**，並**擴充功能以提升使用者體驗**。建議按優先級順序實施。

---

## 2. 優先處理事項 (安全性強化)

以下是應**立即處理**的嚴重安全風險，以確保生產環境的穩定與安全。

### 2.1. 使用環境變數管理敏感資訊

- **問題:** `SECRET_KEY`、資料庫憑證等敏感資訊被硬編碼在 `settings.py` 中。
- **建議:**
    1.  安裝 `python-dotenv` 函式庫來管理環境變數。
    2.  在專案根目錄建立 `.env` 檔案，並將敏感資訊移入其中。
        ```
        # .env
        DEBUG=False
        SECRET_KEY='your-production-secret-key'
        DATABASE_URL='postgres://postgres:postgres@bes-rds:5432/postgres'
        ```
    3.  修改 `settings.py`，從環境變數中讀取這些值。
    4.  將 `.env` 檔案加入 `.gitignore`，避免提交到版本控制中。

### 2.2. 關閉 DEBUG 模式並設定 ALLOWED_HOSTS

- **問題:** 生產環境中不應啟用 `DEBUG` 模式。
- **建議:**
    1.  在 `.env` 檔案中設定 `DEBUG=False`。
    2.  在 `settings.py` 中，根據環境變數設定 `ALLOWED_HOSTS`，例如 `ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')`。

---

## 3. 維護性與部署優化

這些建議旨在簡化開發流程，降低長期維護成本。

### 3.1. 統一相依性管理

- **問題:** `pyproject.toml` 和 `requirements.txt` 同時存在，容易導致版本不一致。
- **建議:**
    1.  **刪除 `requirements.txt` 檔案。**
    2.  以 `pyproject.toml` 作為唯一的相依性來源。
    3.  開發時使用 `uv pip install <package>` 來新增套件，`uv` 會自動更新 `pyproject.toml`。
    4.  在部署腳本或 `Dockerfile` 中，統一使用 `uv sync --frozen` 來安裝相依套件，確保環境一致性。

### 3.2. 分離不同環境的設定檔

- **問題:** 所有環境 (開發、生產) 共用一份 `settings.py`。
- **建議:**
    1.  將 `settings.py` 拆分為 `base.py`, `development.py`, `production.py`。
    2.  `base.py` 存放通用設定。
    3.  `development.py` 繼承 `base.py` 並包含開發專用設定 (如 `django-debug-toolbar`)。
    4.  `production.py` 繼承 `base.py` 並包含生產專用設定 (如 `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`)。
    5.  透過環境變數 `DJANGO_SETTINGS_MODULE` 來指定要使用的設定檔。

---

## 4. 功能擴充建議

在完成上述優化後，可考慮以下功能來提升網站價值。

### 4.1. 訂單管理與查詢功能

- **現狀:** 使用者下單後，缺乏一個查看歷史訂單的介面。
- **建議:**
    1.  在 `accounts` 或 `orders` app 中，建立一個「我的訂單」頁面。
    2.  該頁面應列出使用者的所有歷史訂單，包含訂單編號、日期、總金額、狀態等。
    3.  提供訂單詳情頁，展示該筆訂單的具體商品項目與收件資訊。

### 4.2. 非同步任務處理 (Celery + Redis)

- **場景:** 未來若需要處理耗時任務 (如寄送大量電子郵件通知、產生報表)，直接在 Django request-response 週期中處理會影響效能。
- **建議:**
    1.  引入 `Celery` 和 `Redis`。
    2.  將耗時操作（例如，訂單確認 Email 的寄送）改為非同步任務。
    3.  這能顯著提升使用者操作的反應速度，並增強系統的穩定性。

### 4.3. 完善付款流程 (整合金流服務)

- **現狀:** 目前的付款流程僅是標記為「已付款」，並未實際對接金流。
- **建議:**
    1.  研究並選擇一個適合的第三方金流服務 (如 Stripe, NewebPay, Line Pay)。
    2.  在 `orders` app 中，開發與金流 API 對接的邏輯。
    3.  在 `create_order` 後，將使用者導向金流服務的付款頁面，並在接收到付款成功的回調通知後，才將訂單狀態更新為 `paid=True`。

### 4.4. 增加網站後台儀表板 (Dashboard)

- **現狀:** 管理員功能分散在 Django Admin 中。
- **建議:**
    1.  建立一個客製化的後台儀表板頁面。
    2.  儀表板可以視覺化呈現關鍵指標，如：每日訂單數、銷售總額、熱門點燈項目等。
    3.  這將有助於營運者快速掌握網站狀況。

## 5. 總結

BESSOW 專案目前已具備穩固的基礎。本建議書提出的方案旨在協助專案走向生產就緒狀態，並為未來的可持續發展提供清晰的路線圖。建議從**安全性強化**開始，逐步推進**維護性優化**與**功能擴充**，以確保專案的長期成功。
