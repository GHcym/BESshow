# 優化-更新EC2的authorized_keys 步驟 1：檢查當前狀態

## 具體操作指令
檢查EC2伺服器的連線狀態、現有公鑰設定，以及新舊私鑰的狀況。

## 輸入參數與說明
- EC2地址：43.198.12.223
- 使用者：ubuntu
- 舊私鑰：/tmp/besshow-key-backup.pem（備份檔案）
- 新私鑰：.key/besshow-key.pem
- 新公鑰：.key/besshow-key.pub

## 執行步驟

### 1.1 檢查新公鑰內容
```bash
$ cat .key/besshow-key.pub
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs/1NDndWKdKdG0hSGWx2
L9cZ4aYxadDTlOgfWCv1SUOj1Y84ahEtllW8P+fJKTYoCBWnzdtP4IKw5KjPQy7H
...
-----END PUBLIC KEY-----
```
✅ 新公鑰已生成

### 1.2 測試舊私鑰連線
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "whoami"
Connection successful with old key
ubuntu
```
✅ 舊私鑰仍可正常連線EC2

### 1.3 檢查EC2現有授權
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "cat ~/.ssh/authorized_keys"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCx4zh2nD4I7SC3j7KE4PdPqM2tOQzhlq3BCLqhhc7bjwUj0emgyFDCfVsbLgyy56awpDoV6YDZMJSsp9i7wxaUXqjeJi4T6ZvZvDykGQQwXF9Q1xNGKB0UN7Y0Fie1mrkAUXwwb9m1jmpnMYq9LATsCTVuFSpvo/kshxSfrkZrxlzcQ0knxxR9kKoR+Id5CY/yltxHzuak7fcvB+rjzo9ZcOj1+Ca1ZcKfNbVBlRJgxVpufP4jS1cnT459Ymb6dd+98bGiSNvp4zV8FjYhskXfgb/8xdeHUN+VkicRWOSW8h0pkF3PFkWFZepIK8aL2iCNBviIs1Y+p2t1bVmp+NJx besshow-key
```
📝 發現一個舊公鑰授權（besshow-key）

### 1.4 測試新私鑰連線
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "echo 'New key works'"
ubuntu@43.198.12.223: Permission denied (publickey).
```
❌ 新私鑰無法連線（預期結果）

### 1.5 生成新SSH公鑰格式
```bash
$ ssh-keygen -y -f .key/besshow-key.pem
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCz/U0Od1Yp0p0bSFIZbHYv1xnhpjFp0NOU6B9YK/VJQ6PVjzhqES2WVbw/58kpNigIFafN20/ggrDkqM9DLsdB4KAqODpiTGIfDET9elwb5/rJXWz6e7/pgNXMKEi6cieStOpX9UVkN2Ednwdzv6HlsYbyuzyhw4bpCHAddogj1rppuISlXHMMQ8Z4gAfYYu285bzBYIO1JGWJ1vSdnvG7nbqKdUPaEKdzFUfihdUzbuE7VNKsdklhWQmpLe506chBwHpfLvJifGB27b1D6hcjxnlg0gpfuOdF0bo53L9uCrVltD7haO/erVW7lOo+1xunfCq7RcrEbxnEU/CwcaYt
```
✅ 新SSH公鑰格式已生成

## 輸出結果與說明

### 當前狀態分析
- **舊私鑰狀態**：✅ 仍可連線EC2
- **新私鑰狀態**：❌ 無法連線（未授權）
- **EC2授權數量**：1個舊公鑰
- **安全風險**：🔴 舊私鑰仍有效，存在安全隱患

### 需要執行的操作
1. 備份現有authorized_keys
2. 添加新公鑰到授權清單
3. 測試新私鑰連線
4. 移除舊公鑰授權

### 關鍵資訊
- **舊公鑰指紋**：...+NJx besshow-key
- **新公鑰指紋**：...caYt（待添加）
- **EC2地址**：43.198.12.223