#!/bin/bash
# Django 管理指令便利腳本
# 使用方式: ./scripts/manage.sh migrate
#          ./scripts/manage.sh createsuperuser
#          ./scripts/manage.sh shell

set -e

# 檢查是否在正確的目錄
if [ ! -f "docker-compose.yml" ]; then
    echo "錯誤: 請在專案根目錄執行此腳本"
    exit 1
fi

# 執行 Django 管理指令
docker compose exec bes-app python manage.py "$@"