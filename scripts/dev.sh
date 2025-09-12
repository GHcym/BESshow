#!/bin/bash
# 開發環境便利腳本
# 使用方式: ./scripts/dev.sh up    # 啟動服務
#          ./scripts/dev.sh down  # 停止服務
#          ./scripts/dev.sh logs  # 查看日誌
#          ./scripts/dev.sh shell # 進入容器

set -e

case "$1" in
    up)
        echo "=== 啟動開發環境 ==="
        docker compose up -d
        echo "服務已啟動，訪問 http://localhost:8000"
        ;;
    down)
        echo "=== 停止開發環境 ==="
        docker compose down
        ;;
    build)
        echo "=== 重新建構映像 ==="
        docker compose up --build -d
        ;;
    logs)
        docker compose logs -f bes-app
        ;;
    shell)
        docker compose exec bes-app bash
        ;;
    migrate)
        echo "=== 執行資料庫遷移 ==="
        docker compose exec bes-app python manage.py migrate
        ;;
    superuser)
        echo "=== 建立超級用戶 ==="
        docker compose exec bes-app python manage.py createsuperuser
        ;;
    *)
        echo "使用方式: $0 {up|down|build|logs|shell|migrate|superuser}"
        echo ""
        echo "指令說明:"
        echo "  up        - 啟動開發環境"
        echo "  down      - 停止開發環境"
        echo "  build     - 重新建構並啟動"
        echo "  logs      - 查看應用程式日誌"
        echo "  shell     - 進入容器 shell"
        echo "  migrate   - 執行資料庫遷移"
        echo "  superuser - 建立超級用戶"
        exit 1
        ;;
esac