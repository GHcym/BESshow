# Task: 首頁「立即點燈」修正 (shou-ye-li-ji-dian-deng-xiu-zheng)

## 任務指令

1.  **問題分析**：修正首頁「立即點燈」功能。
2.  **步驟拆解**：
    - [x] 步驟 1: 了解首頁「立即點燈」功能的相關程式碼。
        - 具體操作指令: `search_file_content` 或 `glob` 配合 `read_file`
        - 預期輸出結果: 相關檔案內容
        - 必要輸入參數: `pattern`, `include`, `path` 或 `absolute_path`
    - [x] 步驟 2: 根據問題分析結果，修改相關程式碼。
        - 具體操作指令: `replace` 或 `write_file`
        - 預期輸出結果: 程式碼修改完成
        - 必要輸入參數: `file_path`, `old_string`, `new_string` 或 `content`
    - [x] 步驟 3: 建立 `shou-ye-li-ji-dian-deng-xiu-zheng-Code-Changes-20250909.diff` 檔案，記錄程式碼變更。
        - 具體操作指令: `run_shell_command` (`git diff`)
        - 預期輸出結果: `.diff` 檔案建立成功
        - 必要輸入參數: `command`
    - [x] 步驟 4: 更新 `shou-ye-li-ji-dian-deng-xiu-zheng-PROCESS-20250909.md` 檔案，標記已完成的步驟。
        - 具體操作指令: `replace`
        - 預期輸出結果: `PROCESS` 檔案更新成功
        - 必要輸入參數: `file_path`, `old_string`, `new_string`
    - [ ] 步驟 5: 建立 `shou-ye-li-ji-dian-deng-xiu-zheng-DONE-20250909.md` 檔案，總結任務執行結果。
        - 具體操作指令: `write_file`
        - 預期輸出結果: `DONE` 檔案建立成功
        - 必要輸入參數: `file_path`, `content`
