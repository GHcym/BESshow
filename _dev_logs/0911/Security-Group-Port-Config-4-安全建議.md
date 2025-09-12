# 步驟 4：安全性最佳實務

## 🔒 安全群組設定最佳實務

### 最小權限原則
- **僅開放必要連接埠**：只開放應用程式實際需要的連接埠
- **限制來源 IP**：避免使用 `0.0.0.0/0`，改用特定 IP 或 IP 範圍
- **定期檢查規則**：移除不再需要的規則

### SSH 存取安全
```bash
# ❌ 不安全：開放給所有 IP
--cidr 0.0.0.0/0

# ✅ 安全：僅開放給您的 IP
--cidr YOUR_IP/32

# ✅ 更安全：使用 AWS Systems Manager Session Manager
# 完全不需要開放 SSH 連接埠
```

### 資料庫安全
```bash
# ❌ 危險：資料庫開放給所有 IP
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 3306 --cidr 0.0.0.0/0

# ✅ 安全：僅開放給應用伺服器
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 3306 --source-group sg-app-server
```

### 動態 IP 解決方案
```bash
# 取得當前公有 IP
MY_IP=$(curl -s https://checkip.amazonaws.com)

# 使用當前 IP 設定規則
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 22 \
  --cidr ${MY_IP}/32
```

## 🛡️ 安全檢查清單

### 開放前檢查
- [ ] 確認連接埠確實需要
- [ ] 檢查來源 IP 限制
- [ ] 考慮使用安全群組引用而非 CIDR
- [ ] 評估是否可使用 VPN 或 AWS PrivateLink

### 定期維護
- [ ] 每月檢查安全群組規則
- [ ] 移除不再使用的規則
- [ ] 檢查過於寬鬆的規則 (0.0.0.0/0)
- [ ] 使用 AWS Config 監控變更

## ⚠️ 常見安全風險

### 高風險設定
```bash
# 🚨 極度危險：開放所有連接埠給所有 IP
--protocol tcp --port 0-65535 --cidr 0.0.0.0/0

# 🚨 危險：SSH 開放給所有 IP
--protocol tcp --port 22 --cidr 0.0.0.0/0

# 🚨 危險：資料庫開放給所有 IP
--protocol tcp --port 3306 --cidr 0.0.0.0/0
```

### 替代安全方案
- **AWS Systems Manager Session Manager**：無需 SSH 連接埠
- **AWS VPN**：安全的遠端存取
- **AWS PrivateLink**：私有服務連接
- **Bastion Host**：跳板機架構