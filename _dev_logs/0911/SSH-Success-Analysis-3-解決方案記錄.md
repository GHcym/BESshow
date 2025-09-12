# 步驟 3：解決方案記錄

## ✅ 正確的 SSH 連線方法

### 標準連線指令
```bash
ssh -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62
```

### 詳細參數說明
- `-i ./.key/bes-ec2-1.pem`：指定私鑰檔案路徑
- `ubuntu`：Ubuntu AMI 的預設用戶名
- `43.213.18.62`：EC2 實例的公有 IP

## 🛠️ 完整設定檢查清單

### 1. 安全群組設定 ✅
```bash
# 檢查安全群組規則
aws ec2 describe-security-groups --group-ids sg-00be696b3cc144425

# 確認 SSH 連接埠開放
# Type: SSH, Protocol: TCP, Port: 22, Source: 0.0.0.0/0 或您的 IP
```

### 2. 私鑰檔案設定 ✅
```bash
# 檢查檔案存在
ls -la ./.key/bes-ec2-1.pem

# 確認權限正確 (400 或 600)
chmod 400 ./.key/bes-ec2-1.pem
```

### 3. 實例狀態確認 ✅
```bash
# 檢查實例狀態
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].State.Name'
```

## 🔧 故障排除步驟

### 如果連線失敗，按順序檢查：

#### 1. 網路連通性
```bash
# 測試連接埠
nc -zv 43.213.18.62 22
```

#### 2. 用戶名確認
```bash
# Ubuntu AMI
ssh -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62

# Amazon Linux AMI
ssh -i ./.key/bes-ec2-1.pem ec2-user@43.213.18.62
```

#### 3. 詳細診斷
```bash
# 使用詳細模式
ssh -v -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62
```

## 📋 快速連線腳本
```bash
#!/bin/bash
# SSH 連線到 BES EC2 實例

INSTANCE_IP="43.213.18.62"
KEY_FILE="./.key/bes-ec2-1.pem"
USERNAME="ubuntu"

# 檢查私鑰檔案
if [ ! -f "$KEY_FILE" ]; then
    echo "錯誤：私鑰檔案不存在 $KEY_FILE"
    exit 1
fi

# 設定正確權限
chmod 400 "$KEY_FILE"

# 連線
ssh -i "$KEY_FILE" "$USERNAME@$INSTANCE_IP"
```