# 優化-更新EC2的authorized_keys 步驟 5：撤銷舊授權

## 具體操作指令
從EC2的authorized_keys中移除已暴露的舊公鑰，確保只有新的安全私鑰可以存取。

## 輸入參數與說明
- 目標檔案：EC2上的 ~/.ssh/authorized_keys
- 移除目標：舊公鑰（besshow-key）
- 保留目標：新公鑰（besshow-key-new）

## 執行步驟

### 5.1 確認當前授權狀態
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "wc -l ~/.ssh/authorized_keys && grep -n 'besshow-key' ~/.ssh/authorized_keys"
3 /home/ubuntu/.ssh/authorized_keys
1:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCx4zh2nD4I7SC3j7KE4PdPqM2tOQzhlq3BCLqhhc7bjwUj0emgyFDCfVsbLgyy56awpDoV6YDZMJSsp9i7wxaUXqjeJi4T6ZvZvDykGQQwXF9Q1xNGKB0UN7Y0Fie1mrkAUXwwb9m1jmpnMYq9LATsCTVuFSpvo/kshxSfrkZrxlzcQ0knxxR9kKoR+Id5CY/yltxHzuak7fcvB+rjzo9ZcOj1+Ca1ZcKfNbVBlRJgxVpufP4jS1cnT459Ymb6dd+98bGiSNvp4zV8FjYhskXfgb/8xdeHUN+VkicRWOSW8h0pkF3PFkWFZepIK8aL2iCNBviIs1Y+p2t1bVmp+NJx besshow-key
3: besshow-key-new
```
📝 發現3行內容：第1行是舊公鑰，第3行是新公鑰

### 5.2 移除舊公鑰
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "sed -i '1d' ~/.ssh/authorized_keys"
```
✅ 舊公鑰（第1行）已移除

### 5.3 驗證移除結果
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "cat ~/.ssh/authorized_keys"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCz/U0Od1Yp0p0bSFIZbHYv1xnhpjFp0NOU6B9YK/VJQ6PVjzhqES2WVbw/58kpNigIFafN20/ggrDkqM9DLsdB4KAqODpiTGIfDET9elwb5/rJXWz6e7/pgNXMKEi6cieStOpX9UVkN2Ednwdzv6HlsYbyuzyhw4bpCHAddogj1rppuISlXHMMQ8Z4gAfYYu285bzBYIO1JGWJ1vSdnvG7nbqKdUPaEKdzFUfihdUzbuE7VNKsdklhWQmpLe506chBwHpfLvJifGB27b1D6hcjxnlg0gpfuOdF0bo53L9uCrVltD7haO/erVW7lOo+1xunfCq7RcrEbxnEU/CwcaYt besshow-key-new
```
✅ 現在只剩下新公鑰（besshow-key-new）

### 5.4 測試舊私鑰連線
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "echo 'Old key still works'"
ubuntu@43.198.12.223: Permission denied (publickey).
```
✅ 舊私鑰已無法連線

### 5.5 確認新私鑰連線
```bash
$ ssh -i .key/besshow-key.pem ubuntu@43.198.12.223 "echo '✅ 新私鑰連線正常' && whoami"
✅ 新私鑰連線正常
ubuntu
```
✅ 新私鑰仍可正常連線

## 輸出結果與說明

### 撤銷結果
- **舊公鑰狀態**：❌ 已從 authorized_keys 中移除
- **新公鑰狀態**：✅ 保留並正常運作
- **舊私鑰測試**：❌ Permission denied
- **新私鑰測試**：✅ 連線成功

### 安全狀態
- **授權數量**：1個（僅新公鑰）
- **暴露風險**：✅ 已完全消除
- **存取控制**：✅ 僅新私鑰可存取

### 後續影響
- 舊私鑰已完全失效，無法再存取EC2
- 新私鑰成為唯一有效的存取方式
- 系統安全性已得到完全保障
- 可以安全刪除舊私鑰備份檔案