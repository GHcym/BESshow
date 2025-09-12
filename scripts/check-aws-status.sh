#!/bin/bash

echo "🔍 Checking AWS staging environment status..."

# 檢查網站可用性
echo "📡 Testing website accessibility..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://43.198.12.223:8000)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Website is accessible (HTTP $HTTP_CODE)"
else
    echo "❌ Website returned HTTP $HTTP_CODE"
fi

# 檢查管理後台
echo "🔐 Testing admin panel..."
ADMIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://43.198.12.223:8000/admin/)
if [ "$ADMIN_CODE" = "302" ]; then
    echo "✅ Admin panel is accessible (redirects to login)"
else
    echo "❌ Admin panel returned HTTP $ADMIN_CODE"
fi

# 檢查容器狀態
echo "🐳 Checking container status..."
ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 \
    "cd /home/ubuntu/besshow && docker compose -f docker-compose.staging.yml ps"

# 檢查系統資源
echo "💻 Checking system resources..."
ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 \
    "echo 'Memory usage:' && free -h && echo 'Disk usage:' && df -h /"

echo "📊 Status check completed!"