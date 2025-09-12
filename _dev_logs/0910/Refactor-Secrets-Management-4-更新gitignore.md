# Step 4: 更新 .gitignore

**日期:** 2025年09月10日

## 目的

將 `.env` 檔案加入到 `.gitignore` 忽略清單中，以防止包含敏感資訊的環境變數檔案被意外提交到版本控制系統（如 Git）中。

## 執行過程

### 1. 讀取 `.gitignore`

我首先讀取了專案根目錄下的 `.gitignore` 檔案的現有內容。

### 2. 新增忽略規則

我在檔案末尾追加了 `_env` 規則，並附上註解說明其用途。

- **修改前 (部分內容):**
```
# Screencast
Lithium_Demo_2025.mp4
```

- **修改後 (部分內容):**
```
# Screencast
Lithium_Demo_2025.mp4

# Environment variables
.env
```

## 產出

- `.gitignore` 檔案已更新，現在會忽略 `.env` 檔案。
