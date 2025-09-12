# 步驟 4：問題診斷

## 安全群組檢查結果

### 安全群組 ID
- **Group ID**: sg-00be696b3cc144425

### 入站規則分析
```
連接埠 22 (SSH):   ✅ 已開放 (僅限同安全群組)
連接埠 80 (HTTP):  ✅ 已開放 (僅限同安全群組)  
連接埠 443 (HTTPS): ✅ 已開放 (僅限同安全群組)
```

## 🔍 問題根本原因

### 發現的問題
**安全群組規則限制過嚴**：
- SSH (22) 只允許來自同一安全群組的流量
- 沒有開放給外部 IP 存取
- 來源設定為 `UserIdGroupPairs` 而非 `CidrIp`

### 具體說明
```
當前設定：Source = sg-00be696b3cc144425 (僅限同安全群組)
需要設定：Source = 0.0.0.0/0 或您的 IP/32
```

## 🛠️ 解決方案

### 方法 1：開放給所有 IP (快速但較不安全)
```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-00be696b3cc144425 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

### 方法 2：僅開放給您的 IP (建議)
```bash
# 取得您的公有 IP
MY_IP=$(curl -s https://checkip.amazonaws.com)

# 開放給您的 IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-00be696b3cc144425 \
  --protocol tcp \
  --port 22 \
  --cidr ${MY_IP}/32
```

### 方法 3：AWS Console 操作
1. EC2 Console → Security Groups
2. 選擇 sg-00be696b3cc144425
3. Edit inbound rules
4. 修改 SSH 規則的 Source 為 0.0.0.0/0 或您的 IP

## 📋 測試步驟
修復後的測試順序：
1. 修改安全群組規則
2. 等待 1-2 分鐘生效
3. 重新測試連接埠：`nc -zv 43.213.18.62 22`
4. SSH 連線測試：`ssh -i bes-ec2-1.pem ec2-user@43.213.18.62`

## 🎯 診斷結論
- **實例狀態**：✅ 正常運行
- **網路設定**：✅ 有公有 IP
- **安全群組**：❌ SSH 規則限制過嚴
- **解決方案**：修改安全群組入站規則