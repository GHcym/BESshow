# 步驟 4：最佳實務

## 🔒 SSH 連線安全最佳實務

### 1. 私鑰管理
```bash
# 設定正確權限
chmod 400 ~/.ssh/private-key.pem

# 安全存放位置
mkdir -p ~/.ssh
mv private-key.pem ~/.ssh/
```

### 2. SSH 配置檔案
建立 `~/.ssh/config` 簡化連線：
```
Host bes-ec2
    HostName 43.213.18.62
    User ubuntu
    IdentityFile ~/.ssh/bes-ec2-1.pem
    IdentitiesOnly yes
```

使用方式：
```bash
ssh bes-ec2
```

### 3. 安全群組最佳實務
```bash
# 僅開放給您的 IP (建議)
MY_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
  --group-id sg-00be696b3cc144425 \
  --protocol tcp --port 22 --cidr ${MY_IP}/32

# 避免開放給所有 IP (0.0.0.0/0)
```

## 🛡️ 進階安全設定

### 1. 使用 Session Manager (無需 SSH)
```bash
# 安裝 Session Manager Plugin
# 然後使用
aws ssm start-session --target i-07f5692f52fb7d948
```

### 2. SSH 金鑰輪換
```bash
# 定期更換金鑰對
aws ec2 create-key-pair --key-name new-key-pair
# 更新實例的 authorized_keys
# 刪除舊金鑰對
```

### 3. 多重驗證
```bash
# 在實例上設定 MFA
sudo apt install libpam-google-authenticator
```

## 📊 連線監控

### 1. CloudTrail 記錄
- 監控 EC2 API 呼叫
- 追蹤安全群組變更

### 2. VPC Flow Logs
- 監控網路流量
- 分析連線模式

### 3. 系統日誌
```bash
# 在實例上檢查 SSH 日誌
sudo tail -f /var/log/auth.log
```

## 🔧 故障排除工具

### 1. AWS CLI 診斷
```bash
# 檢查實例狀態
aws ec2 describe-instance-status --instance-ids i-07f5692f52fb7d948

# 檢查系統日誌
aws ec2 get-console-output --instance-id i-07f5692f52fb7d948
```

### 2. 網路診斷
```bash
# 測試連接埠
nmap -p 22 43.213.18.62

# 追蹤路由
traceroute 43.213.18.62
```

### 3. SSH 診斷
```bash
# 詳細模式
ssh -vvv -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62

# 測試不同驗證方法
ssh -o PreferredAuthentications=publickey -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62
```

## 📋 檢查清單範本

### 連線前檢查
- [ ] 實例狀態為 running
- [ ] 安全群組開放 SSH (22)
- [ ] 私鑰檔案存在且權限正確
- [ ] 使用正確的用戶名
- [ ] 網路連通性正常

### 連線後檢查
- [ ] 系統更新：`sudo apt update`
- [ ] 安全設定：檢查防火牆規則
- [ ] 監控設定：確認日誌記錄
- [ ] 備份設定：定期備份重要資料