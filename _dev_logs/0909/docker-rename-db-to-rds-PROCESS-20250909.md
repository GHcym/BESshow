# Task: docker-rename-db-to-rds

## 任務指令

1.  **問題分析**：將 Docker 服務名稱從 `bes-db` 修改為 `bes-rds`。
2.  **步驟拆解**：
    - [x] 步驟 1: 讀取 `docker-compose.yml` 檔案內容。
        - 具體操作指令: `read_file`
        - 預期輸出結果: `docker-compose.yml` 的內容
        - 必要輸入參數: `absolute_path`
    - [x] 步驟 2: 在 `docker-compose.yml` 中將 `bes-db` 服務定義替換為 `bes-rds`。
        - 具體操作指令: `replace`
        - 預期輸出結果: `docker-compose.yml` 檔案更新成功
        - 必要輸入參數: `file_path`, `old_string`, `new_string`
    - [x] 步驟 3: 在 `docker-compose.yml` 中將 `depends_on: - bes-db` 替換為 `depends_on: - bes-rds`。
        - 具體操作指令: `replace`
        - 預期輸出結果: `docker-compose.yml` 檔案更新成功
        - 必要輸入參數: `file_path`, `old_string`, `new_string`
    - [x] 步驟 4: 建立 `docker-rename-db-to-rds-Code-Changes-20250909.diff` 檔案，記錄程式碼變更。
        - 具體操作指令: `run_shell_command` (`git diff`)
        - 預期輸出結果: `.diff` 檔案建立成功
        - 必要輸入參數: `command`
    - [x] 步驟 5: 更新 `Plan-PROCESS-docker-rename-db-to-rds-20250909.md` 檔案，標記已完成的步驟。
        - 具體操作指令: `replace`
        - 預期輸出結果: `PROCESS` 檔案更新成功
        - 必要輸入參數: `file_path`, `old_string`, `new_string`
    - [ ] 步驟 6: 建立 `Plan-DONE-docker-rename-db-to-rds-20250909.md` 檔案，總結任務執行結果。
        - 具體操作指令: `write_file`
        - 預期輸出結果: `DONE` 檔案建立成功
        - 必要輸入參數: `file_path`, `content`
