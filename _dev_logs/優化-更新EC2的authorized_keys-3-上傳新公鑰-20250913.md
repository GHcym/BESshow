# 優化-更新EC2的authorized_keys 步驟 3：上傳新公鑰

## 具體操作指令
將新生成的SSH公鑰添加到EC2的authorized_keys檔案中，使新私鑰能夠連線。

## 輸入參數與說明
- 新公鑰來源：本地 .key/besshow-key.pem（轉換為SSH格式）
- 目標位置：EC2 ~/.ssh/authorized_keys
- 操作方式：追加（不覆蓋現有內容）

## 執行步驟

### 3.1 生成SSH格式的新公鑰
```bash
$ ssh-keygen -y -f .key/besshow-key.pem > /tmp/new-public-key.pub
$ echo " besshow-key-new" >> /tmp/new-public-key.pub
$ cat /tmp/new-public-key.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCz/U0Od1Yp0p0bSFIZbHYv1xnhpjFp0NOU6B9YK/VJQ6PVjzhqES2WVbw/58kpNigIFafN20/ggrDkqM9DLsdB4KAqODpiTGIfDET9elwb5/rJXWz6e7/pgNXMKEi6cieStOpX9UVkN2Ednwdzv6HlsYbyuzyhw4bpCHAddogj1rppuISlXHMMQ8Z4gAfYYu285bzBYIO1JGWJ1vSdnvG7nbqKdUPaEKdzFUfihdUzbuE7VNKsdklhWQmpLe506chBwHpfLvJifGB27b1D6hcjxnlg0gpfuOdF0bo53L9uCrVltD7haO/erVW7lOo+1xunfCq7RcrEbxnEU/CwcaYt besshow-key-new
```
✅ 新SSH公鑰已生成（標記為 besshow-key-new）

### 3.2 上傳新公鑰到EC2
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "cat >> ~/.ssh/authorized_keys" < /tmp/new-public-key.pub
```
✅ 新公鑰已添加到authorized_keys

### 3.3 驗證authorized_keys內容
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "cat ~/.ssh/authorized_keys"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCx4zh2nD4I7SC3j7KE4PdPqM2tOQzhlq3BCLqhhc7bjwUj0emgyFDCfVsbLgyy56awpDoV6YDZMJSsp9i7wxaUXqjeJi4T6ZvZvDykGQQwXF9Q1xNGKB0UN7Y0Fie1mrkAUXwwb9m1jmpnMYq9LATsCTVuFSpvo/kshxSfrkZrxlzcQ0knxxR9kKoR+Id5CY/yltxHzuak7fcvB+rjzo9ZcOj1+Ca1ZcKfNbVBlRJgxVpufP4jS1cnT459Ymb6dd+98bGiSNvp4zV8FjYhskXfgb/8xdeHUN+VkicRWOSW8h0pkF3PFkWFZepIK8aL2iCNBviIs1Y+p2t1bVmp+NJx besshow-key
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCz/U0Od1Yp0p0bSFIZbHYv1xnhpjFp0NOU6B9YK/VJQ6PVjzhqES2WVbw/58kpNigIFafN20/ggrDkqM9DLsdB4KAqODpiTGIfDET9elwb5/rJXWz6e7/pgNXMKEi6cieStOpX9UVkN2Ednwdzv6HlsYbyuzyhw4bpCHAddogj1rppuISlXHMMQ8Z4gAfYYu285bzBYIO1JGWJ1vSdnvG7nbqKdUPaEKdzFUfihdUzbuE7VNKsdklhWQmpLe506chBwHpfLvJifGB27b1D6hcjxnlg0gpfuOdF0bo53L9uCrVltD7haO/erVW7lOo+1xunfCq7RcrEbxnEU/CwcaYt besshow-key-new
```
📝 現在有兩個公鑰：舊的（besshow-key）和新的（besshow-key-new）

### 3.4 測試新私鑰連線
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "echo 'New key connection successful!' && whoami"
New key connection successful!
ubuntu
```
✅ 新私鑰連線成功！

## 輸出結果與說明

### 上傳結果
- **新公鑰狀態**：✅ 已成功添加
- **連線測試**：✅ 新私鑰可正常連線
- **授權數量**：2個（舊 + 新）
- **安全狀態**：🟡 部分安全（舊私鑰仍有效）

### 現在的授權清單
1. **舊公鑰**：...+NJx besshow-key（待移除）
2. **新公鑰**：...caYt besshow-key-new（已添加）

### 後續影響
- 新私鑰已可用於部署腳本
- 需要移除舊公鑰以完成安全更新
- 可以開始測試新私鑰的所有功能