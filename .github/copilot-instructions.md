# BESshow AI Coding Agent Instructions

## 專案架構與核心知識
- 本專案為「廟宇祈福網站」MVP，基於 `wsvincent/lithium` Django 範本，採多 app 結構：
  - `accounts/`：用戶管理與認證（整合 django-allauth）
  - `products/`：燈種資料 CRUD
  - `cart/`：購物車功能，context processor 提供全域 cart 狀態
  - `orders/`：訂單管理
  - `pages/`：靜態頁面（首頁、關於等）
- 前端採 Bootstrap 5，所有主要頁面皆繼承 `_base.html`，美化與響應式設計統一於此。
- 所有 app 皆有獨立的 `models.py`, `views.py`, `urls.py`, `templates/`，遵循 Django 標準慣例。

## 開發與運行流程
- 開發環境以 Docker 管理，主要服務：
  - `bes-web`：Django 應用，啟動時使用 gunicorn（見 Dockerfile）
  - `bes-db`：PostgreSQL 資料庫
- 啟動/重啟指令：
  ```bash
  docker compose -f besshow/docker-compose.yml up --build -d
  docker compose -f besshow/docker-compose.yml exec bes-web python manage.py migrate
  docker compose -f besshow/docker-compose.yml exec bes-web python manage.py createsuperuser
  docker compose -f besshow/docker-compose.yml down
  ```
- 進入容器進行除錯或手動操作：
  ```bash
  docker exec -it bes-web bash
  ```
- 所有資料庫遷移、管理指令均需在容器內執行。

## 重要慣例與模式
- 所有頁面美化、表單渲染統一使用 Bootstrap 5 與 crispy-forms（`{{ form|crispy }}`），避免巢狀 `<form>`。
- Template 路徑必須為 `app/templates/app/xxx.html`，並用 `{% extends '_base.html' %}`。
- context processor `cart.context_processors.cart_context` 會自動注入購物車資訊至所有 template。
- 所有 app 需在 `INSTALLED_APPS` 註冊，template 自動尋找於 app 目錄。
- 靜態檔案統一放於 `static/`，媒體檔案於 `media/`。

## 測試與除錯
- 測試檔案於各 app 的 `tests.py`，可用 Django 測試框架執行。
- 除錯時可用 `DEBUG=True`，並啟用 `debug_toolbar`。
- 若 template 未正確渲染，請檢查 extends、block 名稱、Docker volume 掛載與容器內檔案同步。

## 典型檔案/目錄
- `docker-compose.yml`、`Dockerfile`：環境建置與服務定義
- `manage.py`、`django_project/settings.py`：專案主設定
- `accounts/`、`products/`、`cart/`、`orders/`、`pages/`：主要功能 app
- `templates/_base.html`：全站統一外觀
- `static/`、`media/`：靜態與媒體資源

---
如需跨 app 資料流、特殊開發流程或自訂模式，請參考 `README.md` 或各 app 內註解。
