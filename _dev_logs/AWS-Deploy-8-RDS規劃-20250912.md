# AWS-Deploy 步驟 8：RDS規劃

## 具體操作指令
制定 PostgreSQL 從 Docker 容器遷移到 AWS RDS 的詳細計劃

## 輸入參數與說明
- 分析當前 Docker PostgreSQL 配置
- 設計 AWS RDS 架構
- 制定數據遷移策略
- 規劃生產環境部署流程

## 輸出結果與說明
- 完成 PostgreSQL 從 Docker 容器遷移到 AWS RDS 的完整規劃
- 建立詳細的遷移計劃文件與自動化腳本
- 提供成本估算、風險評估與回滾策略
- 生產環境 Docker 配置已準備完成
- 下一步：可以按照計劃實施 RDS 遷移

📝 **RDS 遷移規劃要點**：
- **成本**：約 $20/月 (db.t3.micro + 20GB 儲存)
- **停機時間**：< 30 分鐘
- **實施時程**：3 週 (準備 → 測試 → 正式遷移)
- **主要檔案**：RDS-Migration-Plan-20250912.md, migrate-to-rds.sh
- **回滾計劃**：保留 Docker 容器備份 7 天

## 執行步驟

### 8.1 分析當前資料庫配置
```bash
$ docker compose -f docker-compose.staging.yml exec bes-rds psql -U besshow -d besshow -c '\l'
# 資料庫清單：besshow, postgres, template0, template1

$ docker compose -f docker-compose.staging.yml exec bes-rds psql -U besshow -d besshow -c '\dt'
# 18 個表格：用戶、產品、訂單、購物車等

$ docker compose -f docker-compose.staging.yml exec bes-rds psql -U besshow -d besshow -c "SELECT pg_size_pretty(pg_database_size('besshow'));"
 database_size: 8916 kB
```
✅ 當前資料庫狀態分析完成
- PostgreSQL 16, UTF8 編碼
- 資料庫大小：8.9 MB
- 18 個表格，包含完整的 Django 應用程式結構

### 8.2 設計 RDS 架構
✅ AWS RDS 配置建議
- **引擎**：PostgreSQL 16.x
- **實例類型**：db.t3.micro (測試) → db.t3.small (生產)
- **儲存**：20 GB gp3
- **成本估算**：約 $20/月

### 8.3 建立遷移計劃
✅ 完整遷移策略文件已建立
- 檔案：RDS-Migration-Plan-20250912.md
- 包含 4 個階段的詳細實施計劃
- 風險評估與回滾計劃

### 8.4 準備生產環境配置
✅ 生產環境檔案已建立
- docker-compose.prod.yml：使用外部 RDS
- migrate-to-rds.sh：自動化遷移腳本
- 移除 PostgreSQL 容器，新增 Redis 快取