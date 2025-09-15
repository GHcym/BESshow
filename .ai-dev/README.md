# AI 開發助理系統架構

## 目錄結構
```
/.ai-dev/                           # AI 開發助理根目錄
├── system/                         # 系統核心
│   ├── prompts/                   # Prompt 系統
│   │   ├── base.md               # 基礎設定
│   │   ├── modes/                # 工作模式
│   │   │   ├── quick.md         # 快速問答模式
│   │   │   ├── task.md          # 任務追蹤模式
│   │   │   └── learn.md         # 學習指導模式
│   │   └── specialists/          # 專業模組
│   │       ├── django.md        # Django 專家
│   │       ├── frontend.md      # 前端專家
│   │       └── devops.md        # DevOps 專家
│   ├── config/                   # 系統配置
│   │   ├── project.json         # 專案配置
│   │   └── preferences.json     # 使用者偏好
│   └── templates/               # 文件範本
│       ├── task-template.md     # 任務範本
│       └── report-template.md   # 報告範本
├── workspace/                    # 工作空間
│   ├── active/                  # 進行中任務
│   ├── archive/                 # 已完成任務
│   └── logs/                    # 執行日誌
├── knowledge/                   # 知識庫
│   ├── concepts/               # 技術概念
│   ├── patterns/               # 設計模式
│   └── troubleshooting/        # 問題解決
└── reports/                    # 報告系統
    ├── daily/                  # 每日總結
    └── project/                # 專案報告
```

## 設計原則
- **漸進式複雜度**: 從簡單到複雜
- **模組化設計**: 功能獨立，易於擴展
- **實用性優先**: 解決實際問題
- **新手友善**: 降低學習門檻