# Step 1: 安裝相依套件

**日期:** 2025年09月10日

## 目的

為了能夠從 `.env` 檔案中讀取環境變數，我們需要將 `python-dotenv` 函式庫加入專案的相依性清單中。

## 執行過程

### 1. 修改 `pyproject.toml`

我首先讀取了 `pyproject.toml` 檔案，然後使用 `replace` 工具將 `"python-dotenv ~=0.21",` 加入到 `[project.dependencies]` 列表中。

- **修改前:**
```toml
dependencies = [
  "django ~=5.1",
  "django-allauth[openid,socialaccount] ~=65.2",
  "django-debug-toolbar ~=4.4",
  "crispy-bootstrap5 ~=2024.10",
  "gunicorn ~=23.0",
  "psycopg[binary] ~=3.2",
  "whitenoise ~=6.7",
    "pillow ~=11.3",
  "lunar_python ==1.4.4", # Specific version requested for 時辰 support
]
```

- **修改後:**
```toml
dependencies = [
  "django ~=5.1",
  "django-allauth[openid,socialaccount] ~=65.2",
  "django-debug-toolbar ~=4.4",
  "crispy-bootstrap5 ~=2024.10",
  "gunicorn ~=23.0",
  "psycopg[binary] ~=3.2",
  "whitenoise ~=6.7",
  "pillow ~=11.3",
  "lunar_python ==1.4.4", # Specific version requested for 時辰 support
  "python-dotenv ~=0.21",
]
```

### 2. 同步環境

修改設定檔後，我執行了 `uv sync` 指令。這個指令會讀取 `pyproject.toml`，將新的套件 (`python-dotenv`) 安裝到目前的虛擬環境中，並更新 `uv.lock` 檔案以鎖定版本。

- **執行指令:**
```bash
uv sync
```

- **結果:** 指令成功執行，`python-dotenv` 已安裝完成。

## 產出

- `pyproject.toml` 已更新。
- `uv.lock` 已更新。
- 虛擬環境中已包含 `python-dotenv` 函式庫。
