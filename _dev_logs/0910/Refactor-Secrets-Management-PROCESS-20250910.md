# Task: Refactor-Secrets-Management

## TO-DO List
[V] 1_安裝相依套件：將 `python-dotenv` 加入專案相依性。
[V] 2_建立環境變數檔案：建立 `.env` 檔案存放敏感資訊，並建立 `.env.example` 作為範本。
[V] 3_修改設定檔：更新 `django_project/settings.py` 以讀取環境變數。
[V] 4_更新 .gitignore：將 `.env` 檔案加入忽略清單。
[>] 5_驗證變更：確認應用程式在新的設定下能正常啟動與運作。

## Step 1: 安裝相依套件 (Completed)
*   **Action:** Added `python-dotenv` and `dj-database-url` to `pyproject.toml` and synced the environment.
*   **File created:** `Refactor-Secrets-Management-1-安裝相依套件.md`

## Step 2: 建立環境變數檔案 (Completed)
*   **Action:** Created `.env.example` and a `.env` file with a newly generated `SECRET_KEY`.
*   **File created:** `Refactor-Secrets-Management-2-建立環境變數檔案.md`

## Step 3: 修改設定檔 (Completed)
*   **Action:** Modified `django_project/settings.py` to read sensitive information from environment variables.
*   **File created:** `Refactor-Secrets-Management-3-修改設定檔.md`

## Step 4: 更新 .gitignore (Completed)
*   **Action:** Added `.env` to the `.gitignore` file.
*   **File created:** `Refactor-Secrets-Management-4-更新gitignore.md`

## Step 5: 驗證變更
*   **Action:** Restarting the application container and checking logs for errors.