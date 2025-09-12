# 成果總結：除錯-結帳與訂單-A

## 1. 任務名稱

除錯-結帳與訂單-A

## 2. 最終成果

成功修復了使用者在結帳時因個人資料不完整而陷入無限重導向循環的問題。現在，使用者可以順利完成個人資料的填寫，並成功建立訂單。

## 3. 問題根本原因分析 (Root Cause Analysis)

本次除錯發現問題由兩個核心缺陷和一個輔助問題疊加造成：

1.  **表單欄位缺失**：`accounts/forms.py` 中的 `CustomUserUpdateForm` 未包含 `last_name` (姓氏) 欄位。這導致使用者即使提交了表單，也無法將姓氏存入資料庫。

2.  **不完整的資料檢查**：`orders/views.py` 中的 `payment_page` 視圖在載入前會檢查使用者資料的完整性。由於 `last_name` 始終為空，此檢查永遠不會通過，導致使用者在儲存個人資料後，又被立刻重導向回編輯頁面，形成死循環。

3.  **模板錯誤訊息屏蔽**：初期的 `user_profile_form.html` 模板設計不當，無法顯示後端傳回的表單驗證錯誤，增加了早期排查的難度。

## 4. 解決方案

依據除錯過程，依序實施了以下修正：

1.  **強化日誌**：修改了 `orders/views.py` 中的檢查邏輯，使其能在日誌中明確指出是哪個欄位缺失，從而快速定位到 `last_name` 問題。

2.  **修正表單**：在 `accounts/forms.py` 的 `CustomUserUpdateForm` 中，將 `last_name` 補回 `fields` 清單與 `Layout` 中，確保該欄位能被正確處理和儲存。

3.  **修正模板**：修正了 `templates/account/user_profile_form.html`，確保 `crispy-forms` 的錯誤訊息可以被正確渲染。

4.  **導入 `reverse`**：修正了因缺少 `from django.urls import reverse` 導入而引發的 `NameError`。
