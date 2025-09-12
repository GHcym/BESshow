# 步驟 5：SSH連線測試

## 具體操作指令
由於網路連通性測試已失敗，SSH 連線測試無法進行。

## 正常情況下的測試方法
```bash
# 使用私鑰連線
ssh -i /path/to/private-key.pem ec2-user@43.213.18.62

# 詳細模式連線（用於除錯）
ssh -v -i /path/to/private-key.pem ec2-user@43.213.18.62

# 測試連接埠連通性
ssh -o ConnectTimeout=10 -i /path/to/private-key.pem ec2-user@43.213.18.62
```

## 當前狀況
- 網路層面無法連通
- 無法進行 SSH 連線測試
- 需要先解決網路連通性問題

## 常見 SSH 問題
1. **私鑰問題**：
   - 私鑰檔案權限 (chmod 400)
   - 私鑰路徑錯誤
   - 金鑰對不匹配

2. **使用者名稱問題**：
   - Amazon Linux: ec2-user
   - Ubuntu: ubuntu
   - CentOS: centos

3. **連接埠問題**：
   - 預設 SSH 連接埠 22
   - 自訂連接埠設定