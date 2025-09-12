# 步驟 3：SSH 連線測試

## 具體操作指令
由於連接埠測試已失敗，SSH 連線測試無法進行。

## 正常情況下的測試方法
```bash
# 使用私鑰連線 (需要 bes-ec2-1.pem 檔案)
ssh -i /path/to/bes-ec2-1.pem ec2-user@43.213.18.62

# 詳細模式測試
ssh -v -i /path/to/bes-ec2-1.pem ec2-user@43.213.18.62

# 連線逾時測試
ssh -o ConnectTimeout=10 -i /path/to/bes-ec2-1.pem ec2-user@43.213.18.62
```

## 當前狀況
- **連接埠 22 無法連通**：網路層面阻擋
- **無法進行 SSH 連線**：需要先解決網路問題
- **金鑰檔案**：需要 bes-ec2-1.pem 私鑰檔案

## 預期錯誤訊息
如果嘗試 SSH 連線，會看到：
```
ssh: connect to host 43.213.18.62 port 22: Connection timed out
```

## 必要條件
1. **網路連通性**：連接埠 22 必須開放
2. **私鑰檔案**：bes-ec2-1.pem 檔案
3. **正確權限**：私鑰檔案權限 600
4. **正確用戶名**：
   - Amazon Linux: ec2-user
   - Ubuntu: ubuntu
   - CentOS: centos