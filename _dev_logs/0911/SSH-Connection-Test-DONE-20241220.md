# SSH 連線測試任務完成報告

**任務名稱：** SSH-Connection-Test  
**執行日期：** 2024-12-20  
**任務狀態：** ✅ 完成

## 執行計劃
測試 EC2 實例 i-07f5692f52fb7d948 的 SSH 連線，包含：
1. 取得實例資訊
2. 連接埠測試
3. SSH 連線測試
4. 問題診斷

## 執行項目
### 已完成步驟
- [V] 取得實例資訊：確認實例狀態和 IP
- [V] 連接埠測試：測試 SSH 連接埠 22
- [V] SSH 連線測試：分析連線失敗原因
- [V] 問題診斷：找到根本原因和解決方案

### 重要發現
- **實例狀態**：✅ running (正常)
- **公有 IP**：43.213.18.62
- **金鑰對**：bes-ec2-1
- **SSH 連接埠**：❌ 無法連通
- **安全群組**：sg-00be696b3cc144425

## 執行結果
### 🔍 問題診斷結果

#### 實例資訊 ✅
```
狀態：running
公有 IP：43.213.18.62
私有 IP：172.31.35.9
金鑰對：bes-ec2-1
```

#### 連接埠測試 ❌
```
SSH 連接埠 22：Connection timed out
原因：安全群組規則限制
```

#### 安全群組分析 🔍
```
安全群組 ID：sg-00be696b3cc144425
SSH 規則：僅允許同安全群組存取
問題：沒有開放給外部 IP
```

### 🎯 根本原因
**安全群組 SSH 規則限制過嚴**：
- 當前：僅允許同安全群組 (sg-00be696b3cc144425) 存取
- 需要：開放給外部 IP 存取

### 🛠️ 解決方案

#### 立即修復指令
```bash
# 方法 1：開放給您的 IP (建議)
MY_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
  --group-id sg-00be696b3cc144425 \
  --protocol tcp --port 22 --cidr ${MY_IP}/32

# 方法 2：開放給所有 IP (較不安全)
aws ec2 authorize-security-group-ingress \
  --group-id sg-00be696b3cc144425 \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```

#### AWS Console 修復
1. **EC2 Console** → **Security Groups**
2. **選擇** sg-00be696b3cc144425
3. **Edit inbound rules**
4. **修改 SSH 規則**：Source 改為 0.0.0.0/0 或您的 IP

### 📋 修復後測試步驟
```bash
# 1. 測試連接埠
nc -zv 43.213.18.62 22

# 2. SSH 連線 (需要私鑰檔案)
ssh -i /path/to/bes-ec2-1.pem ec2-user@43.213.18.62
```

### 🔑 SSH 連線需求
- **私鑰檔案**：bes-ec2-1.pem
- **檔案權限**：`chmod 600 bes-ec2-1.pem`
- **用戶名**：ec2-user (Amazon Linux)

### 📁 相關文件
- 執行過程：`SSH-Connection-Test-PROCESS-20241220.md`
- 步驟記錄：`SSH-Connection-Test-[1-4]-*.md`