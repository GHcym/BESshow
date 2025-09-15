# Prompt 模式：任務追蹤 (Workflow Mode) - 優化版

## 1. 繼承
本模式繼承 `base_optimized.md` 的所有設定。

## 2. 用途
處理複雜、多階段開發任務，確保可追溯性與可管理性。

## 3. 任務管理流程

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