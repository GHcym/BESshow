# 步驟 2：AWS CLI 指令方法

## ⚡ AWS CLI 快速開放連接埠

### 前置作業
```bash
# 配置 AWS CLI (如果尚未配置)
aws configure

# 查詢實例的安全群組 ID
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text
```

### 開放 SSH (連接埠 22)
```bash
# 開放給所有 IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# 開放給特定 IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32
```

### 開放 HTTP (連接埠 80)
```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```

### 開放 HTTPS (連接埠 443)
```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

### 開放自訂連接埠
```bash
# 開放單一連接埠
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 8080 \
  --cidr 0.0.0.0/0

# 開放連接埠範圍
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 8000-8999 \
  --cidr 0.0.0.0/0
```

### 查詢安全群組規則
```bash
aws ec2 describe-security-groups \
  --group-ids sg-xxxxxxxxx \
  --query 'SecurityGroups[0].IpPermissions'
```

### 移除規則
```bash
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```