# AWS-EC2-Staging-Deploy - 步驟2：EC2實例建立

## 具體操作指令
啟動 t3.micro EC2 實例並設定安全群組

## 輸入參數與說明
- 實例類型：t3.micro (免費額度)
- AMI：Ubuntu Server 22.04 LTS
- 儲存：30GB gp3
- 安全群組：SSH, HTTP, Custom TCP 8000

## 操作步驟

### 2.1 啟動 EC2 實例
1. 前往 **EC2 Dashboard**
2. 確認右上角區域為 **ap-northeast-1 (東京)**
3. 點選 **"Launch Instance"**

### 2.2 設定實例詳細資訊
```
Name: BESshow-Staging-Server

Application and OS Images:
- Quick Start: Ubuntu
- AMI: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
- Architecture: 64-bit (x86)

Instance type:
- t3.micro (符合免費方案條件)

Key pair:
- 選擇現有的 Key pair 或建立新的
- 如建立新的：名稱 "besshow-key"，類型 RSA，格式 .pem
```

### 2.3 網路設定
```
Network settings:
- VPC: default
- Subnet: 任選一個 public subnet
- Auto-assign public IP: Enable

Firewall (security groups):
- Create security group
- Security group name: besshow-staging-sg
- Description: Security group for BESshow staging server

Inbound Security Group Rules:
1. SSH
   - Type: SSH
   - Protocol: TCP
   - Port: 22
   - Source: My IP (會自動填入您的 IP)

2. HTTP  
   - Type: HTTP
   - Protocol: TCP
   - Port: 80
   - Source: Anywhere (0.0.0.0/0)

3. Custom TCP (Django 開發伺服器)
   - Type: Custom TCP
   - Protocol: TCP
   - Port: 8000
   - Source: Anywhere (0.0.0.0/0)
```

### 2.4 儲存設定
```
Configure storage:
- Volume 1 (Root): 
  - Size: 30 GiB (免費額度內)
  - Volume type: gp3
  - Delete on termination: Yes
```

### 2.5 進階詳細資訊 (可選)
```
User data (可選，用於自動安裝基本套件):
#!/bin/bash
apt update
apt install -y curl wget git
```

### 2.6 確認並啟動
1. 檢查 **Summary** 中的所有設定
2. 確認顯示 **"Free tier eligible"**
3. 點選 **"Launch instance"**
4. 等待實例狀態變為 **"Running"**

## 輸出結果與說明

### 記錄重要資訊
完成後請記錄以下資訊：

```
實例資訊:
- Instance ID: i-xxxxxxxxx
- Public IPv4 address: xxx.xxx.xxx.xxx
- Public IPv4 DNS: ec2-xxx-xxx-xxx-xxx.ap-northeast-1.compute.amazonaws.com
- Private IPv4 address: 172.31.x.x

安全群組:
- Security Group ID: sg-xxxxxxxxx
- Name: besshow-staging-sg

Key Pair:
- Name: besshow-key
- 檔案位置: ~/Downloads/besshow-key.pem
```

### 驗證步驟
1. 實例狀態檢查：**Running**
2. 狀態檢查：**2/2 checks passed**
3. 可以 ping 通公開 IP
4. SSH 連線測試成功

### SSH 連線測試
```bash
# 設定 key 檔案權限
chmod 400 ~/Downloads/besshow-key.pem

# 測試 SSH 連線
ssh -i ~/Downloads/besshow-key.pem ubuntu@YOUR_PUBLIC_IP

# 成功連線後會看到 Ubuntu 歡迎訊息
```

### 下一步準備
- 公開 IP 位址：準備用於環境變數設定
- SSH 連線確認：準備進行伺服器初始化
- 安全群組設定完成：網路存取已就緒

## 故障排除

### 常見問題
1. **無法 SSH 連線**
   - 檢查安全群組 SSH 規則
   - 確認 Key pair 檔案權限 (chmod 400)
   - 確認使用正確的用戶名 (ubuntu)

2. **免費額度警告**
   - 確認選擇 t3.micro
   - 確認儲存空間 ≤ 30GB
   - 檢查是否在免費額度期間內

3. **實例啟動失敗**
   - 檢查 VPC 和 Subnet 設定
   - 確認區域選擇正確
   - 檢查帳戶限制