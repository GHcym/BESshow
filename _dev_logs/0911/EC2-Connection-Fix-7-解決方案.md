# 步驟 7：解決方案

## 🛠️ 立即執行步驟

### 1. 檢查實例狀態 (最優先)
```bash
# 登入 AWS Console
# 前往 EC2 → Instances
# 搜尋 i-07f5692f52fb7d948
# 檢查 Instance State
```

**如果實例已停止**：
- 點擊 "Start instance"
- 等待狀態變為 "running"
- 重新測試連線

### 2. 檢查安全群組設定
```bash
# 在 EC2 Console 中
# 選擇實例 → Security tab → Security groups
# 檢查 Inbound rules
```

**必要規則**：
```
Type: SSH, Protocol: TCP, Port: 22, Source: 0.0.0.0/0
Type: HTTP, Protocol: TCP, Port: 80, Source: 0.0.0.0/0
Type: HTTPS, Protocol: TCP, Port: 443, Source: 0.0.0.0/0
```

### 3. 檢查網路 ACL (如果安全群組正常)
```bash
# VPC Console → Network ACLs
# 檢查與實例子網路關聯的 ACL
# 確認 Inbound/Outbound rules 允許必要流量
```

### 4. 系統層級診斷 (如果網路正常)
```bash
# 使用 AWS Systems Manager Session Manager
# 或 EC2 Serial Console 存取實例
# 檢查內部防火牆和服務狀態
```

## 🔧 AWS CLI 解決方案 (需要配置憑證)

### 配置 AWS CLI
```bash
aws configure
# 輸入 Access Key ID
# 輸入 Secret Access Key  
# 輸入 Region (如: ap-northeast-1)
# 輸入 Output format (json)
```

### 檢查實例狀態
```bash
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].State.Name'
```

### 啟動實例 (如果已停止)
```bash
aws ec2 start-instances --instance-ids i-07f5692f52fb7d948
```

### 檢查安全群組
```bash
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId'
```

## 📋 檢查清單

- [ ] 實例狀態是否為 "running"
- [ ] 安全群組是否開放 SSH (22)
- [ ] 安全群組是否開放 HTTP (80)
- [ ] 網路 ACL 是否允許流量
- [ ] 路由表是否有網際網路閘道
- [ ] 實例是否有公有 IP
- [ ] SSH 金鑰是否正確

## ⚡ 快速修復指令

如果確認是安全群組問題：
```bash
# 開放 SSH 存取
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```