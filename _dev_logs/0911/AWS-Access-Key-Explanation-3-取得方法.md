# 步驟 3：取得方法

## 🛠️ 如何取得 AWS Access Key ID

### 方法 1：AWS Console (建議)

#### 步驟
1. **登入 AWS Console**
   - 前往 [AWS Console](https://console.aws.amazon.com)

2. **進入 IAM 服務**
   - 搜尋並點擊 "IAM"

3. **建立或選擇用戶**
   - 點擊 "Users" → "Create user" (新用戶)
   - 或選擇現有用戶

4. **建立 Access Key**
   - 選擇用戶 → "Security credentials" 標籤
   - 點擊 "Create access key"
   - 選擇使用案例 (CLI, SDK, etc.)

5. **下載憑證**
   - **重要**：Secret Access Key 只會顯示一次
   - 點擊 "Download .csv file" 保存

### 方法 2：AWS CLI (需要現有憑證)
```bash
# 建立新的 Access Key (需要權限)
aws iam create-access-key --user-name MyUser
```

### 方法 3：Root 用戶 Access Key (不建議)
1. 登入 Root 帳戶
2. 右上角帳戶名稱 → "Security credentials"
3. "Access keys" 區段 → "Create access key"

## 📋 建立時的選項

### 使用案例選擇
- **Command Line Interface (CLI)**
- **Local code**
- **Application running on AWS compute service**
- **Application running outside AWS**
- **Other**

### 最佳實務標籤
建議加上標籤：
```
Key: Purpose, Value: CLI-Access
Key: Environment, Value: Development
Key: Owner, Value: YourName
```

## ⚠️ 重要提醒
- **Secret Access Key 只顯示一次**：建立後立即保存
- **Root 用戶不建議**：建立 IAM 用戶使用
- **定期輪換**：建議每 90 天更換一次
- **最小權限**：只給予必要的權限