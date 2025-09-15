# Django 模板管理指南

## 問題描述
Django 模板搜尋順序容易造成混淆，導致修改錯誤的模板檔案。

## 解決方案

### 1. 統一使用 App 層級模板 (推薦)
```
✅ 優點：
- 模板與 app 邏輯緊密結合
- 避免命名衝突
- 易於維護和除錯

❌ 缺點：
- 需要在每個 app 中重複建立目錄結構
```

### 2. 明確的命名規範
```
✅ 優點：
- 集中管理所有模板
- 清楚的檔案命名避免混淆

❌ 缺點：
- 需要嚴格遵守命名規範
- 大型專案中檔案數量龐大
```

## 實作規範

### 檔案命名規範
```
# App 層級模板
accounts/templates/accounts/
├── account_form.html          # 管理員編輯帳號
├── user_profile_form.html     # 使用者編輯個人資料
└── account_list.html          # 帳號列表

# Project 層級模板 (僅共用)
templates/
├── _base.html                 # 基礎模板
├── 404.html                   # 錯誤頁面
└── 500.html
```

### 檢查工具
```bash
# 檢查模板衝突
find . -name "*.html" -path "*/templates/*" | sort

# 檢查特定模板位置
find . -name "account_form.html" -path "*/templates/*"
```

### View 中明確指定模板
```python
class AccountUpdateView(UpdateView):
    template_name = 'accounts/account_form.html'  # 明確指定
    # 而不是依賴 Django 自動搜尋
```

## 除錯技巧

### 1. 模板註解
```html
<!-- Template: accounts/templates/accounts/account_form.html -->
{% extends '_base.html' %}
```

### 2. 檢查指令
```bash
# 找出重複模板
find . -name "*.html" -path "*/templates/*" | xargs basename -a | sort | uniq -d
```

## 本專案現狀
- ✅ 已移除重複的 project 層級 account_form.html
- ✅ 統一使用 app 層級模板
- ✅ 建立備份檔案 (account_form.html.backup)