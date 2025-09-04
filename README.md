# BESshow (廟宇祈福網站)

本專案為一個現代化且功能完整的「廟宇網站」最小可行性產品（MVP）。
主要目標是讓信眾可以線上點燈並完成付款。

本專案基於 `wsvincent/lithium` 範本進行開發。

---

## 開發環境設定 (Local Development Setup)

本專案使用 Docker 進行開發環境管理，請確保您的系統已安裝 Docker 與 Docker Compose。

### 啟動步驟

1.  **啟動服務**

    在專案的根目錄 (`/home/ksu/bess`) 下，執行以下指令來建構並啟動 `bes-web` 和 `bes-db` 服務：

    ```bash
    docker compose -f besshow/docker-compose.yml up --build -d
    ```

2.  **執行資料庫遷移 (Migrate)**

    首次啟動服務時，需要初始化資料庫。在另一個終端機視窗中，執行以下指令來建立資料庫綱要 (Schema)：

    ```bash
    docker compose -f besshow/docker-compose.yml exec bes-web python manage.py migrate
    ```

3.  **建立管理者帳號 (Optional)**

    如果您需要登入後台管理介面，可以建立一個管理者帳號：

    ```bash
    docker compose -f besshow/docker-compose.yml exec bes-web python manage.py createsuperuser
    ```
    接著依照提示輸入帳號、Email 與密碼。

### 訪問網站

-   **前台網站**: [http://localhost:8000](http://localhost:8000)
-   **後台管理**: [http://localhost:8000/admin](http://localhost:8000/admin)

### 停止服務

當您完成開發工作後，可以執行以下指令來停止所有服務：

```bash
docker compose -f besshow/docker-compose.yml down
```

---