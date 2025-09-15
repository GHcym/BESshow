# 優化-更新EC2的authorized_keys 步驟 2：備份舊設定

## 具體操作指令
備份EC2伺服器上的SSH授權設定，確保在更新過程中可以回復到原始狀態。

## 輸入參數與說明
- 備份來源：EC2上的 ~/.ssh/authorized_keys
- 備份位置：本地 /tmp/ 目錄
- 備份格式：帶時間戳的檔案名稱

## 執行步驟

### 2.1 建立本地備份目錄
```bash
$ mkdir -p /tmp/ec2-backup
```
✅ 備份目錄已建立

### 2.2 備份authorized_keys到本地
```bash
$ scp -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223:~/.ssh/authorized_keys /tmp/ec2-backup/authorized_keys.backup.20250913_145454
```
✅ 本地備份完成

### 2.3 在EC2上建立備份
```bash
$ ssh -i /tmp/besshow-key-backup.pem ubuntu@43.198.12.223 "cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.backup.20250913_145506"
$ ls -la ~/.ssh/authorized_keys*
-rw------- 1 ubuntu ubuntu 393 Sep 12 09:39 /home/ubuntu/.ssh/authorized_keys
-rw------- 1 ubuntu ubuntu 393 Sep 13 06:55 /home/ubuntu/.ssh/authorized_keys.backup.20250913_145506
```
✅ EC2上備份完成

### 2.4 驗證備份內容
```bash
$ cat /tmp/ec2-backup/authorized_keys.backup.20250913_145454
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCx4zh2nD4I7SC3j7KE4PdPqM2tOQzhlq3BCLqhhc7bjwUj0emgyFDCfVsbLgyy56awpDoV6YDZMJSsp9i7wxaUXqjeJi4T6ZvZvDykGQQwXF9Q1xNGKB0UN7Y0Fie1mrkAUXwwb9m1jmpnMYq9LATsCTVuFSpvo/kshxSfrkZrxlzcQ0knxxR9kKoR+Id5CY/yltxHzuak7fcvB+rjzo9ZcOj1+Ca1ZcKfNbVBlRJgxVpufP4jS1cnT459Ymb6dd+98bGiSNvp4zV8FjYhskXfgb/8xdeHUN+VkicRWOSW8h0pkF3PFkWFZepIK8aL2iCNBviIs1Y+p2t1bVmp+NJx besshow-key
```
✅ 備份內容驗證正確

## 輸出結果與說明

### 備份結果
- **本地備份**：/tmp/ec2-backup/authorized_keys.backup.20250913_145454
- **EC2備份**：~/.ssh/authorized_keys.backup.20250913_145506
- **備份大小**：393 bytes
- **備份內容**：1個舊公鑰（besshow-key）

### 安全保障
- 雙重備份：本地 + EC2
- 時間戳記：便於識別版本
- 權限保持：600（僅擁有者可讀寫）

### 後續影響
- 可安全進行公鑰更新
- 如有問題可快速回復原始設定