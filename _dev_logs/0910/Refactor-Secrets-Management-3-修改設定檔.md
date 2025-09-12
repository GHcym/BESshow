# Step 3: 修改設定檔

**日期:** 2025年09月10日

## 目的

修改 `django_project/settings.py` 檔案，使其不再包含任何硬編碼的敏感資訊，而是從 `.env` 檔案中讀取這些設定。

## 執行過程

### 1. 新增相依套件 `dj-database-url`

為了方便地從一個 URL 解析資料庫連線資訊，我額外安裝了 `dj-database-url` 函式庫。

- **Action:** 將 `"dj-database-url ~=2.1",` 加入 `pyproject.toml`。
- **Command:** `uv sync`
- **Result:** 套件安裝成功。

### 2. 修改 `settings.py`

我透過一系列的替換操作，逐步將 `settings.py` 改造為讀取環境變數的結構。

#### a. 引入必要模組

在檔案開頭加入了 `os`, `dotenv`, 和 `dj_database_url`。

```python
from pathlib import Path
import os
import dotenv
import dj_database_url
```

#### b. 載入 `.env` 檔案

在 `BASE_DIR` 定義後，立即呼叫 `dotenv.load_dotenv()` 來載入環境變數。

```python
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))
```

#### c. 替換 `SECRET_KEY`

將寫死的金鑰替換為從環境變數讀取。

```python
# old: SECRET_KEY = "django-insecure-0peo@#x9jur3!h$ryje!$879xww8y1y66jx!%*#ymhg&jkozs2"
# new:
SECRET_KEY = os.getenv("SECRET_KEY")
```

#### d. 替換 `DEBUG`

將布林值替換為從環境變數讀取，並處理字串到布林值的轉換。

```python
# old: DEBUG = True
# new:
DEBUG = os.getenv("DEBUG", "False") == "True"
```

#### e. 替換 `ALLOWED_HOSTS`

將寫死的列表替換為從環境變數讀取一個逗號分隔的字串，並將其分割成列表。

```python
# old: ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
# new:
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
```

#### f. 替換 `DATABASES`

將整個 `DATABASES` 字典替換為使用 `dj_database_url` 從 `DATABASE_URL` 環境變數進行解析。

```python
# old: Hardcoded DATABASES dictionary
# new:
DATABASES = {
    "default": dj_database_url.parse(os.getenv("DATABASE_URL"))
}
```

## 產出

- `django_project/settings.py` 檔案已被完全重構，不再包含敏感資訊。
