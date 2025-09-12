# 任務總結：Docker-ReName-RUN-ERROR

## 執行計畫

本次任務旨在解決 Docker 服務（`bes-web` -> `bes-app`, `bes-db` -> `bes-rds`）更名後，導致 Django 應用程式無法啟動的問題。分析認為問題根源在於 Django 設定檔中殘留舊的資料庫主機名稱。

## 執行項目

1.  **檢查 `docker-compose.yml`**：確認服務名稱已更新為 `bes-app` 和 `bes-rds`。
2.  **檢查 `settings.py`**：發現資料庫 `HOST` 仍設定為舊的 `bes-db`。
3.  **更新 `settings.py`**：將資料庫 `HOST` 修改為新的 `bes-rds`。
4.  **重建 Docker 服務**：執行 `docker compose up -d --build` 套用變更。
5.  **驗證修復**：透過 `docker compose exec bes-app python manage.py showmigrations` 指令，確認應用程式已能成功連線至資料庫。

## 執行結果

問題已成功解決。`bes-app` 服務現在可以正常連線到 `bes-rds` 資料庫。使用者現在可以透過 `docker compose exec bes-app python manage.py runserver 0.0.0.0:8000` 成功啟動 Django 開發伺服器。
