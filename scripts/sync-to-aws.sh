#!/bin/bash

echo "🔄 Starting sync to AWS staging environment..."

# 檢查必要檔案
if [ ! -f ".key/besshow-key.pem" ]; then
    echo "❌ SSH key not found: .key/besshow-key.pem"
    exit 1
fi

# 同步檔案到 EC2
echo "📁 Syncing files..."
rsync -avz --progress \
    -e "ssh -i .key/besshow-key.pem -o StrictHostKeyChecking=no" \
    --exclude='_dev_logs' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='media' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='.aider*' \
    ./ ubuntu@43.198.12.223:/home/ubuntu/besshow/

# 重新部署應用程式
echo "🚀 Redeploying application..."
ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 \
    "cd /home/ubuntu/besshow && ./scripts/deploy-staging.sh"

# 檢查部署狀態
echo "🔍 Checking deployment status..."
ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 \
    "cd /home/ubuntu/besshow && docker compose -f docker-compose.staging.yml ps"

echo "✅ Sync completed!"
echo "🌐 Test site: http://43.198.12.223:8000"