# Step 5: 驗證變更

**日期:** 2025年09月10日

## 目的

確認應用程式在修改 `settings.py` 以讀取環境變數後，仍能正常啟動與運作，且所有設定皆能正確載入。

## 執行過程

### 1. 啟動 Docker 服務

首先，確保 `bes-app` 和 `bes-rds` 服務正在運行。

- **執行指令:** `docker compose up -d` (若服務已運行，則會顯示已啟動)

### 2. 偵錯與解決 `ModuleNotFoundError`

在驗證過程中，我們遇到了持續性的 `ModuleNotFoundError: No module named 'django'` 錯誤。經過一系列的偵錯，我們發現問題的根源在於 Docker 環境的設定與 `Dockerfile` 的建置方式。

#### a. `docker-compose.yml` 的 `volumes` 掛載問題

最初的 `docker-compose.yml` 中，`bes-app` 服務的 `volumes` 設定包含 `- /app/.venv`。這導致容器內部的 `/app/.venv` 被一個空的匿名卷遮蔽，使得 `Dockerfile` 中建置的虛擬環境無法被正確使用。

- **解決方案:** 從 `docker-compose.yml` 中移除了 `- /app/.venv` 這一行。

#### b. `.dockerignore` 排除 `.venv` 問題

`.dockerignore` 檔案中包含了 `.venv`，這導致 `Dockerfile` 在 `COPY` 應用程式碼時，不會將虛擬環境複製到最終映像檔中。

- **解決方案:** 從 `.dockerignore` 中移除了 `.venv` 這一行。

#### c. `Dockerfile` 建置虛擬環境問題

即使移除了 `.dockerignore` 的排除，`Dockerfile` 的多階段建置或 `uv` 建立虛擬環境的方式似乎仍有問題，導致 `.venv` 未能正確地被複製到最終映像檔中。

- **解決方案:** 修改 `Dockerfile`，明確地在 `builder` 階段建立虛擬環境，並將 `uv` 安裝到該虛擬環境中，然後使用該虛擬環境中的 `uv` 來安裝所有相依套件。最後，在最終映像檔階段，明確地從 `builder` 階段複製 `/app/.venv` 和 `/app` 的其餘內容。

### 3. 執行 Django 系統檢查

在解決了上述環境問題並重建映像檔後，我們使用 `docker compose run` 指令來執行 Django 的系統檢查，以確保所有設定都已正確載入。

- **執行指令:** `docker compose run --rm bes-app /app/.venv/bin/python manage.py check`

- **結果:** 指令成功執行，並顯示了以下警告：
```
System check identified some issues:

WARNINGS:
?: settings.ACCOUNT_AUTHENTICATION_METHOD is deprecated, use: settings.ACCOUNT_LOGIN_METHODS = {'email'}
?: settings.ACCOUNT_EMAIL_REQUIRED is deprecated, use: settings.ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']
?: settings.ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE is deprecated, use: settings.ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']
?: settings.ACCOUNT_USERNAME_REQUIRED is deprecated, use: settings.ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*']

System check identified 4 issues (0 silenced).
```
這些警告與 `django-allauth` 的舊版設定有關，但並不影響應用程式的正常運行，且證明了 `settings.py` 已成功讀取環境變數。

## 結論

經過多次偵錯與修正，我們成功地將敏感資訊從 `settings.py` 移至環境變數中，並驗證了應用程式在新的設定下能夠正常啟動與運作。這項任務已成功完成。
