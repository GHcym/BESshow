# 步驟 2：問題總結

## 🔍 之前失敗的根本原因

### 主要問題：用戶名錯誤
```bash
# ❌ 錯誤用戶名
ssh -i bes-ec2-1.pem ec2-user@43.213.18.62
# 結果：Permission denied (publickey)

# ✅ 正確用戶名  
ssh -i ./.key/bes-ec2-1.pem ubuntu@43.213.18.62
# 結果：成功連線
```

### 次要問題：檔案路徑
```bash
# ❌ 錯誤路徑
bes-ec2-1.pem

# ✅ 正確路徑
./.key/bes-ec2-1.pem
```

## 📋 問題發生順序回顧

### 1. 網路層問題 (已解決)
- **問題**：安全群組 SSH 規則限制過嚴
- **症狀**：Connection timed out
- **解決**：修改安全群組開放 SSH 連接埠

### 2. 驗證層問題 (剛解決)
- **問題**：用戶名和檔案路徑錯誤
- **症狀**：Permission denied (publickey)
- **解決**：使用正確用戶名 `ubuntu` 和路徑 `./.key/bes-ec2-1.pem`

## 🎯 常見 AMI 用戶名對照

| AMI 類型 | 預設用戶名 |
|----------|------------|
| Amazon Linux | ec2-user |
| Ubuntu | ubuntu |
| CentOS | centos |
| RHEL | ec2-user |
| SUSE | ec2-user |
| Debian | admin |

## 💡 學習重點

### 診斷順序
1. **網路層**：連接埠是否開放
2. **傳輸層**：SSH 服務是否運行
3. **應用層**：用戶名和金鑰是否正確

### 錯誤訊息解讀
- `Connection timed out` → 網路/安全群組問題
- `Permission denied (publickey)` → 驗證問題 (用戶名/金鑰)
- `Host key verification failed` → 主機金鑰問題