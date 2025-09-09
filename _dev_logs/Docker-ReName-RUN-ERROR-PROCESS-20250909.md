# 任務清單：Docker-ReName-RUN-ERROR

- [x] **步驟 1：檢查 `docker-compose.yml` 服務名稱**
  - **操作：** 讀取 `docker-compose.yml` 檔案。
  - **預期結果：** 確認服務名稱已更新為 `bes-app` 和 `bes-rds`。

- [x] **步驟 2：檢查 Django 資料庫設定**
  - **操作：** 讀取 `django_project/settings.py` 檔案。
  - **預期結果：** 找出 `DATABASES` 設定中的 `HOST` 值，預期它仍然是舊的 `bes-db`。

- [x] **步驟 3：更新 Django 資料庫主機設定**
  - **操作：** 修改 `django_project/settings.py`，將 `DATABASES` 設定中的 `HOST` 從 `bes-db` 更新為 `bes-rds`。
  - **預期結果：** 成功更新設定檔。

- [x] **步驟 4：重建並重新啟動 Docker 服務**
  - **操作：** 執行 `docker compose up -d --build` 指令。
  - **預期結果：** Docker 容器成功重建並在背景啟動。

- [x] **步驟 5：驗證服務是否正常運行**
  - **操作：** 執行 `docker compose exec bes-app python manage.py showmigrations` 來驗證資料庫連線。
  - **預期結果：** 指令成功執行並列出遷移狀態，無 `OperationalError`。
