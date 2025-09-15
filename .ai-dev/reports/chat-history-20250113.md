# Chat History - AI 開發助理系統設計 (2025-01-14)

## 會話摘要
**日期**: 2025-01-14  
**主題**: 設計並建立完整的 AI 開發助理系統  
**參與者**: Web 開發新手 + AI 助理  
**目標**: 建立實用的 AI Prompt 系統與目錄架構  

## 討論重點

### 1. 現有系統分析
- **檔案位置**: `besshow/.gemini/prompts/`
- **現有檔案**: 
  - `1.GEMINI+base.md` - 核心指導原則
  - `mode_default.md` - 即時問答模式  
  - `mode_workflow.md` - 任務追蹤模式
- **問題識別**: 工具函數不匹配、過度複雜的狀態管理

### 2. 外部系統評估
- **評估對象**: 全自動化 AI Agent 系統建議
- **優點**: 系統化設計、學習導向、安全意識
- **缺點**: 過度複雜、實現困難、維護負擔高
- **結論**: 不建議完全採用，選擇性借鑑概念

### 3. 最終系統設計

#### 目錄架構
```
/.ai-dev/                           # AI 開發助理根目錄
├── system/                         # 系統核心
│   ├── prompts/                   # Prompt 系統
│   │   ├── base.md               # 基礎設定
│   │   ├── main.md               # 主要整合 Prompt
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

#### 三種工作模式
1. **Quick Mode**: 簡單問答、程式碼片段
2. **Task Mode**: 複雜任務、完整追蹤
3. **Learn Mode**: 深度學習、概念建構

#### Amazon Q 整合
- **Rules**: `.amazonq/rules/ai-assistant.md` (自動載入)
- **Saved Prompts**: `~/.aws/amazonq/prompts/` (手動載入)
- **檔案引用**: `@file` 語法 (按需載入)

## 關鍵決策

### 設計原則
- **漸進式複雜度**: 從簡單到複雜
- **模組化設計**: 功能獨立，易於擴展
- **實用性優先**: 解決實際問題
- **新手友善**: 降低學習門檻

### 技術選擇
- **工具函數**: 使用 Amazon Q 實際可用工具
- **狀態管理**: 檔案系統為主，JSON 為輔
- **文件格式**: Markdown + YAML Front Matter
- **任務追蹤**: 簡化版狀態標記系統

## 產出檔案清單

### 核心系統檔案
- `/.ai-dev/README.md` - 系統架構說明
- `/.ai-dev/system/prompts/base.md` - 基礎設定
- `/.ai-dev/system/prompts/main.md` - 主要整合 Prompt
- `/.ai-dev/system/config/project.json` - 專案配置

### 工作模式檔案
- `/.ai-dev/system/prompts/modes/quick.md` - 快速問答模式
- `/.ai-dev/system/prompts/modes/task.md` - 任務追蹤模式
- `/.ai-dev/system/prompts/modes/learn.md` - 學習指導模式

### 專業模組檔案
- `/.ai-dev/system/prompts/specialists/django.md` - Django 專家模組

### 範本檔案
- `/.ai-dev/system/templates/task-template.md` - 任務文件範本

### Amazon Q 整合檔案
- `.amazonq/rules/ai-assistant.md` - 核心規則 (自動載入)
- `~/.aws/amazonq/prompts/task-mode.md` - 任務模式 Prompt

### 說明文件
- `/.ai-dev/USAGE.md` - 使用指南

## 後續建議

### 實施步驟
1. **Phase 1**: 使用核心 Rules 和基礎 Prompts
2. **Phase 2**: 測試三種工作模式
3. **Phase 3**: 完善知識庫和專業模組
4. **Phase 4**: 優化使用體驗

### 維護重點
- 定期更新專案配置
- 持續完善知識庫
- 收集使用反饋
- 調整模式切換邏輯

## 會話結論
成功設計了一個平衡實用性與功能性的 AI 開發助理系統，適合 Web 開發新手逐步學習與成長。系統採用漸進式設計，避免了過度複雜的問題，同時保持了良好的擴展性。