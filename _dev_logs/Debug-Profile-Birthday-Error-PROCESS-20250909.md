# 任務清單：Debug-Profile-Birthday-Error

- [x] **步驟 1：識別並分析相關檔案**
  - **操作：** 讀取 `accounts/urls.py`, `accounts/views.py`, `accounts/forms.py`, `accounts/models.py`, 和 `templates/account/user_profile_form.html`。
  - **預期結果：** 找出處理個人資料編輯的 URL、View、Form、Model 欄位及 Template 結構。

- [x] **步驟 2：分析 Model (`accounts/models.py`)**
  - **操作：** 檢查 `CustomUser` 模型中生日欄位的名稱與類型。
  - **預期結果：** 確認欄位為 `DateField` 或類似類型。

- [x] **步驟 3：分析 View (`accounts/views.py`)**
  - **操作：** 檢查個人資料編輯視圖是否正確地將使用者實例 (instance) 傳遞給表單。
  - **預期結果：** 找到類似 `form = UserProfileForm(instance=request.user)` 的程式碼。

- [x] **步驟 4：分析 Form (`accounts/forms.py`)**
  - **操作：** 檢查 `UserProfileForm` 是否正確包含生日欄位，並特別注意其 `widget` 設定。
  - **預期結果：** 找出問題根源，很可能在於 `widget` 未能正確渲染 `DateField` 的值。

- [x] **步驟 5：分析 Template (`templates/account/user_profile_form.html`)**
  - **操作：** 檢查模板中如何渲染表單欄位。
  - **預期結果：** 確認表單欄位是透過標準方式 (如 `{{ form.as_p }}` 或 `{{ form.field }}`) 渲染。

- [x] **步驟 6：制定並應用修復方案**
  - **操作：** 根據分析結果，修改 `accounts/forms.py`，為生日欄位明確指定一個能正確處理日期格式的 widget，例如 `forms.DateInput(attrs={'type': 'date'})`。
  - **預期結果：** 成功修改表單設定。

- [x] **步驟 7：產生變更紀錄與總結報告**
  - **操作：** 生成本次變更的 `.diff` 檔案與最終的 `-DONE-` 報告。
  - **預期結果：** 產出所有必要的任務成果文件。
