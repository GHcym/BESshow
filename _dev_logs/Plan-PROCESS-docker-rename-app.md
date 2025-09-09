# 任務執行過程：docker-rename-app

## 任務指令
1.  **問題分析**：用戶要求將專案中 Docker 相關的 `bes-web` 命名修改為 `bes-app`。但目前發現 `docker-compose.dev.yml` 位於 `/home/ksu/projects/temple-app/`，需要先將其移回當前專案目錄，並確保 `docker compose up` 命令使用此檔案。
2.  **步驟拆解**：
    - [x] 步驟 1: 確認 `_dev_logs/` 資料夾存在。
    - [ ] 步驟 2: 將 `/home/ksu/projects/temple-app/docker-compose.dev.yml` 移動到 `/home/ksu/bess/besshow/docker-compose.yml`。
    - [ ] 步驟 3: 確認 `docker-compose.yml` 檔案內容中是否存在 `bes-web`。
    - [ ] 步驟 4: 在 `docker-compose.yml` 中將 `bes-web` 替換為 `bes-app`。
    - [ ] 步驟 5: 讀取並分析 `Dockerfile` 檔案內容。
    - [ ] 步驟 6: 在 `Dockerfile` 中將 `bes-web` 替換為 `bes-app` (如果存在)。
    - [ ] 步驟 7: 執行 Docker 構建命令以驗證更改。
    - [ ] 步驟 8: 執行 Docker 啟動命令以驗證更改。
    - [ ] 步驟 9: 清理舊的 Docker 映像和容器。

## 狀態追蹤