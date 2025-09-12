# AWS-Deploy 步驟 3：Docker配置

## 具體操作指令
準備測試階段 Docker Compose 檔案，適用於 AWS EC2 測試部署

## 輸入參數與說明
- 基於現有的 docker-compose.yml 建立測試版本
- 保持 DEBUG=True (測試階段)
- 配置適合 EC2 環境的網路與端口設定
- 準備測試環境變數檔案

## 執行步驟

### 3.1 檢查現有 Docker 配置
```bash
$ cat docker-compose.yml
# 現有開發環境配置，包含 bes-app 和 bes-rds 服務
```
✅ 現有配置檢查完成
- 服務：bes-app, bes-rds
- 開發環境設定：DEBUG=True

### 3.2 建立測試階段 Docker Compose
```bash
$ cat > docker-compose.staging.yml
# 建立適合 EC2 測試環境的配置
```
✅ 測試階段 Docker Compose 檔案建立成功
- 檔案：docker-compose.staging.yml
- DEBUG=True (測試階段保持除錯模式)
- 配置 EC2 IP 和 DNS

### 3.3 建立測試環境變數
```bash
$ cat > .env.staging
# 建立測試環境變數檔案
```
✅ 測試環境變數檔案建立成功
- 檔案：.env.staging
- 包含資料庫密碼和允許主機設定

### 3.4 建立部署腳本
```bash
$ cat > scripts/deploy-staging.sh
$ chmod +x scripts/deploy-staging.sh
```
✅ 測試階段部署腳本建立成功
- 腳本：scripts/deploy-staging.sh
- 包含完整的部署流程：停止、建置、啟動、遷移

## 輸出結果與說明
- 測試階段 Docker 配置檔案已準備完成
- 環境變數檔案已建立
- 自動化部署腳本已準備就緒
- 下一步：可以開始上傳檔案到 EC2 實例

📝 **重要檔案記錄**：
- docker-compose.staging.yml：測試環境 Docker 配置
- .env.staging：測試環境變數
- scripts/deploy-staging.sh：自動化部署腳本