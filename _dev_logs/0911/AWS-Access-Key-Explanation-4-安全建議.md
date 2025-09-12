# 步驟 4：安全建議

## 🔒 AWS Access Key 安全最佳實務

### 保護憑證
1. **絕不公開分享**
   - 不要放在程式碼中
   - 不要上傳到 GitHub
   - 不要透過 email 傳送

2. **安全儲存**
   ```bash
   # 設定適當的檔案權限
   chmod 600 ~/.aws/credentials
   chmod 600 ~/.aws/config
   ```

3. **使用環境變數**
   ```bash
   export AWS_ACCESS_KEY_ID=<your-key>
   export AWS_SECRET_ACCESS_KEY=<your-secret>
   ```

### 權限管理
1. **最小權限原則**
   - 只給予必要的權限
   - 使用 IAM 政策限制存取

2. **範例限制政策**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "ec2:DescribeInstances",
           "ec2:StartInstances",
           "ec2:StopInstances"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

### 監控和維護
1. **定期檢查**
   ```bash
   # 查看最後使用時間
   aws iam get-access-key-last-used --access-key-id AKIAIOSFODNN7EXAMPLE
   ```

2. **定期輪換**
   - 建議每 90 天更換
   - 建立新的 → 測試 → 刪除舊的

3. **啟用 CloudTrail**
   - 監控 API 呼叫
   - 追蹤異常活動

### 替代方案 (更安全)
1. **IAM Roles**
   ```bash
   # EC2 實例使用 Role，無需 Access Key
   aws ec2 describe-instances  # 自動使用 Role
   ```

2. **AWS SSO**
   ```bash
   # 使用 SSO 登入
   aws sso login --profile my-profile
   ```

3. **臨時憑證**
   ```bash
   # 使用 STS 取得臨時憑證
   aws sts assume-role --role-arn arn:aws:iam::123456789012:role/MyRole
   ```

### 🚨 安全警告標誌
- Access Key 出現在程式碼中
- 權限過於寬鬆 (AdministratorAccess)
- 長期未使用但未刪除
- 在不安全的地方儲存 (如 email, 聊天室)

### 緊急處理
如果 Access Key 洩露：
1. **立即停用**：AWS Console → IAM → Users → Deactivate
2. **建立新的**：產生新的 Access Key
3. **更新應用**：更新所有使用該 Key 的地方
4. **刪除舊的**：確認新的正常運作後刪除