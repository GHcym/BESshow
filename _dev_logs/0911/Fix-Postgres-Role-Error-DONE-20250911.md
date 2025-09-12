# 任務總結：Fix-Postgres-Role-Error

**任務時間：** 2025-09-11

## 執行總結

本次任務成功解決了 Django 應用無法連線至 PostgreSQL 資料庫的問題，錯誤為 `FATAL: role "besshow" does not exist`。

- **根本原因**：Docker volume `besshow_postgres_data` 中包含了一個過時的、未正確初始化的資料庫狀態。該資料庫在建立時未使用正確的 `POSTGRES_USER` 環境變數，導致 `besshow` 這個角色（使用者）沒有被建立。後續的容器啟動僅載入此舊 volume，而忽略了新的環境變數設定。

- **解決方案**：
  1. 執行 `docker compose down` 停止並移除所有相關容器。
  2. 執行 `docker volume rm besshow_postgres_data` 指令，徹底刪除儲存舊資料的 volume。
  3. 執行 `docker compose up -d` 重新啟動服務。此操作會建立一個新的空 volume，觸發 PostgreSQL 容器的初始化腳本，從而使用 `docker-compose.yml` 中定義的 `POSTGRES_USER`、`POSTGRES_DB` 等變數建立全新的資料庫及使用者。

- **驗證方式**：透過執行 `docker compose exec bes-app python manage.py check` 指令，確認 Django 應用程式可以成功連線資料庫，`OperationalError` 不再出現。

## 執行結果

- 成功重設資料庫狀態。
- Django 應用與 PostgreSQL 資料庫之間的連線問題已解決。
