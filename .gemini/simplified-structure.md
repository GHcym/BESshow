# 簡化版 AI Agent 系統架構

## 核心目錄結構
```
/.gemini/
├── prompts/                    # Prompt 系統
│   ├── base.md                # 基礎設定
│   ├── development.md         # 開發模式
│   └── workflow.md            # 工作流程模式
├── state/                     # 狀態管理
│   ├── project-status.json    # 專案狀態
│   └── current-task.json      # 當前任務
├── workspace/                 # 工作空間
│   ├── active/                # 進行中任務
│   └── archive/               # 已完成任務
└── learning/                  # 學習記錄
    ├── concepts/              # 技術概念
    └── practices/             # 最佳實踐
```

## 實現優先級
1. **Phase 1**: 基礎 Prompt + 簡單狀態管理
2. **Phase 2**: 任務追蹤 + 檔案管理
3. **Phase 3**: 學習系統 + 進階功能

## 核心原則
- 最小可行產品 (MVP) 優先
- 漸進式複雜度增加
- 實用性勝過完美性
- 易於維護和理解