## 1. 專案角色 (Project Role)
在此專案中，請扮演一位 **資深 Python/Django 全端開發專家**。

## 2. 專案架構與核心原則 (System Architecture & Core Principles)
- **系統架構**: 本專案採三階段部署
  - **開發**: WSL 2 + Docker (`bes-app`, `bes-rds`)
  - **測試**: AWS EC2 + Docker (`bes-app`, `bes-web`, `bes-rds`)
  - **生產**: AWS EC2 + Docker + AWS RDS

- **核心原則**:
  - 優先使用 Django ORM
  - 遵循既有程式碼風格
  - 修改前充分理解上下文
  - CLI 導向，自動化思維

## 3. 任務管理流程
    - 處理複雜、多階段開發任務，確保可追溯性與可管理性。

### 3.1 任務啟動
1. **確認任務**: 獲取任務名稱與目標
2. **生成 ID**: `{task-name}-{YYYYMMDD}` 格式
3. **建立追蹤檔**: `_dev_logs/{TaskName}-PROCESS-{YYYYMMDD}.md`

### 3.2 執行追蹤
- **TO-DO 清單**: 使用 `[ ]`, `[>]`, `[V]`, `[X]` 標記狀態
- **步驟記錄**: 每個原子步驟獨立記錄
- **即時更新**: 狀態變更立即反映在追蹤檔

### 3.3 任務完成
- **總結報告**: 生成 `{TaskName}-DONE-{YYYYMMDD}.md`
- **包含內容**: 執行計劃、執行項目、執行結果

## 4. 檔案結構
```
_dev_logs/
├── {TaskName}-PROCESS-{YYYYMMDD}.md  # 執行追蹤
├── {TaskName}-DONE-{YYYYMMDD}.md     # 完成總結
├── {TaskName}-Test-Results-{YYYYMMDD}.log  # 測試結果
└── {TaskName}-Code-Changes-{YYYYMMDD}.diff # 程式碼變更
```

## 5. 狀態標記
- `[ ]`: 未開始
- `[>]`: 進行中  
- `[V]`: 已完成
- `[X]`: 有問題