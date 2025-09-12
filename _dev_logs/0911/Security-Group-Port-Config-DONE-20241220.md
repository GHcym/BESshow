# 安全群組連接埠開放設定任務完成報告

**任務名稱：** Security-Group-Port-Config  
**執行日期：** 2024-12-20  
**任務狀態：** ✅ 完成

## 執行計劃
提供完整的 AWS 安全群組連接埠開放設定說明，包含：
1. AWS Console 操作步驟
2. AWS CLI 指令方法
3. 常用連接埠設定
4. 安全性最佳實務

## 執行項目
### 已完成步驟
- [V] AWS Console 操作方法說明
- [V] AWS CLI 指令方法說明
- [V] 常用連接埠對照表
- [V] 安全性最佳實務建議

## 執行結果
### 🎯 完整解決方案

#### 🖥️ AWS Console 方法
1. **EC2 → Security Groups**
2. **選擇安全群組 → Edit inbound rules**
3. **Add rule → 設定 Type/Port/Source**
4. **Save rules**

#### ⚡ AWS CLI 快速指令
```bash
# 開放 SSH (22)
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp --port 22 --cidr YOUR_IP/32

# 開放 HTTP (80)
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```

#### 📋 常用連接埠
- **SSH**: 22
- **HTTP**: 80
- **HTTPS**: 443
- **MySQL**: 3306
- **PostgreSQL**: 5432

#### 🔒 安全建議
- 使用最小權限原則
- 限制來源 IP (避免 0.0.0.0/0)
- 定期檢查和清理規則
- 考慮使用 AWS Systems Manager Session Manager

### 🛠️ 針對 EC2 實例 i-07f5692f52fb7d948 的建議
```bash
# 1. 查詢安全群組 ID
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId'

# 2. 開放 SSH 存取
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp --port 22 --cidr YOUR_IP/32

# 3. 開放 HTTP 存取
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```

### 📁 相關文件
- 執行過程：`Security-Group-Port-Config-PROCESS-20241220.md`
- 步驟記錄：`Security-Group-Port-Config-[1-4]-*.md`