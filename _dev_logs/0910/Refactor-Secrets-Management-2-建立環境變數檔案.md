# Step 2: 建立環境變數檔案

**日期:** 2025年09月10日

## 目的

建立 `.env` 檔案來存放專案的敏感資訊，並建立 `.env.example` 檔案作為團隊協作的範本，同時確保敏感資訊不會被提交到版本控制系統中。

## 執行過程

### 1. 建立 `.env.example` 範本檔案

我首先建立了一個 `.env.example` 檔案，其中包含了必要的環境變數鍵名，但將實際的密鑰留空。這有助於其他開發者了解需要設定哪些變數。

- **產出檔案:** `.env.example`
- **內容:**
```
# .env.example
# This file is an example. Copy it to .env and fill in your actual secrets.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=

# Database URL
# Example for PostgreSQL: postgres://USER:PASSWORD@HOST:PORT/NAME
DATABASE_URL=postgres://postgres:postgres@bes-rds:5432/postgres

# Allowed hosts for production (comma-separated)
# Example: DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### 2. 啟動 Docker 服務

在產生密鑰的過程中，我發現需要透過在 Docker 容器內執行 Django 指令來存取相依套件。由於容器服務當時並未執行，我首先執行了 `docker compose up -d` 來啟動服務。

- **執行指令:**
```bash
docker compose up -d
```
- **結果:** `bes-app` 和 `bes-rds` 服務成功啟動。

### 3. 產生新的 `SECRET_KEY`

為了提高安全性，我使用 `docker compose exec` 在 `bes-app` 容器內部執行 Django 的 `get_random_secret_key` 函式，產生了一個新的隨機密鑰。

- **執行指令:**
```bash
docker compose exec bes-app python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- **產生的密鑰:** `4#q1t*4oxkvi)jbb88s)uk8=+da&(jwbu5g^ovyl+n+(zzt%7-`

### 4. 建立 `.env` 檔案

我將上一步產生的新密鑰以及其他必要的設定寫入了 `.env` 檔案。

- **產出檔案:** `.env`
- **內容:**
```
# .env
# This file contains the actual secrets for the application.
# It should NOT be committed to version control.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='4#q1t*4oxkvi)jbb88s)uk8=+da&(jwbu5g^ovyl+n+(zzt%7-'

# Database URL
DATABASE_URL=postgres://postgres:postgres@bes-rds:5432/postgres

# Allowed hosts for production (comma-separated)
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## 產出

- `.env.example`
- `.env`
