# AWS-EC2-Staging-Deploy - 步驟3：伺服器初始化

## 具體操作指令
SSH 連線到 EC2 並安裝 Docker 環境

## 輸入參數與說明
- 公開 IP：43.213.18.62
- Key Pair：bes-ec2-1
- 用戶名：ubuntu

## 操作步驟

### 3.1 SSH 連線測試
```bash
# 設定 key 檔案權限（在本地執行）
chmod 400 ~/Downloads/bes-ec2-1.pem

# SSH 連線測試
ssh -i ~/Downloads/bes-ec2-1.pem ubuntu@43.213.18.62
```

### 3.2 系統更新（在 EC2 上執行）
```bash
# 更新套件列表
sudo apt update

# 升級系統套件
sudo apt upgrade -y

# 安裝基本工具
sudo apt install -y curl wget git unzip htop
```

### 3.3 安裝 Docker（在 EC2 上執行）
```bash
# 下載 Docker 安裝腳本
curl -fsSL https://get.docker.com -o get-docker.sh

# 執行安裝
sudo sh get-docker.sh

# 將 ubuntu 用戶加入 docker 群組
sudo usermod -aG docker ubuntu

# 啟動 Docker 服務
sudo systemctl enable docker
sudo systemctl start docker
```

### 3.4 安裝 Docker Compose（在 EC2 上執行）
```bash
# 下載 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 設定執行權限
sudo chmod +x /usr/local/bin/docker-compose

# 驗證安裝
docker-compose --version
```

### 3.5 建立目錄結構（在 EC2 上執行）
```bash
# 建立應用程式目錄
sudo mkdir -p /opt/besshow/{data,backups,logs}

# 設定目錄權限
sudo chown -R ubuntu:ubuntu /opt/besshow

# 驗證目錄結構
ls -la /opt/besshow/
```

### 3.6 重新登入套用群組權限
```bash
# 登出
exit

# 重新登入以套用 docker 群組
ssh -i ~/Downloads/bes-ec2-1.pem ubuntu@43.213.18.62

# 驗證 Docker 權限
docker ps
```

## 輸出結果與說明

### 驗證檢查項目
- ✅ SSH 連線成功
- ✅ 系統更新完成
- ✅ Docker 安裝成功
- ✅ Docker Compose 安裝成功
- ✅ 目錄結構建立完成
- ✅ 用戶權限設定正確

### 環境資訊記錄
```
伺服器資訊:
- 公開 IP: 43.213.18.62
- 作業系統: Ubuntu 22.04 LTS
- Docker 版本: (執行後記錄)
- Docker Compose 版本: (執行後記錄)

目錄結構:
/opt/besshow/
├── data/     (資料庫資料)
├── backups/  (備份檔案)
└── logs/     (日誌檔案)
```

### 下一步準備
- 程式碼上傳方式：Git clone 或 SCP
- 環境變數檔案建立
- Docker 服務啟動

## 故障排除

### SSH 連線問題
```bash
# 如果連線被拒絕，檢查安全群組
# 確認 SSH (22) 規則允許您的 IP

# 如果權限錯誤
chmod 400 ~/Downloads/bes-ec2-1.pem

# 如果用戶名錯誤，Ubuntu AMI 使用 ubuntu 用戶
ssh -i ~/Downloads/bes-ec2-1.pem ubuntu@43.213.18.62
```

### Docker 安裝問題
```bash
# 如果 Docker 安裝失敗，手動安裝
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```