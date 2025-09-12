#!/bin/bash
# AWS EC2 部署腳本
# 使用方式: ./scripts/deploy-aws.sh

set -e

echo "=== BESshow AWS EC2 部署腳本 ==="

# 檢查必要檔案
if [ ! -f "docker-compose.staging.yml" ]; then
    echo "錯誤: 找不到 docker-compose.staging.yml"
    exit 1
fi

if [ ! -f ".env.staging" ]; then
    echo "錯誤: 找不到 .env.staging 檔案"
    echo "請先建立 .env.staging 檔案並設定必要的環境變數"
    exit 1
fi

# 載入環境變數
source .env.staging

echo "1. 停止現有服務..."
docker-compose -f docker-compose.staging.yml down || true

echo "2. 建立必要目錄..."
sudo mkdir -p /opt/besshow/{data,backups,logs}
sudo chown -R $USER:$USER /opt/besshow

echo "3. 建構並啟動服務..."
docker-compose -f docker-compose.staging.yml up --build -d

echo "4. 等待服務啟動..."
sleep 30

echo "5. 執行資料庫遷移..."
docker-compose -f docker-compose.staging.yml exec bes-app python manage.py migrate

echo "6. 收集靜態檔案..."
docker-compose -f docker-compose.staging.yml exec bes-app python manage.py collectstatic --noinput

echo "7. 檢查服務狀態..."
docker-compose -f docker-compose.staging.yml ps

echo ""
echo "=== 部署完成 ==="
echo "網站網址: http://$(curl -s ifconfig.me):8000"
echo "管理後台: http://$(curl -s ifconfig.me):8000/admin/"
echo ""
echo "建立管理員帳號:"
echo "docker-compose -f docker-compose.staging.yml exec bes-app python manage.py createsuperuser"