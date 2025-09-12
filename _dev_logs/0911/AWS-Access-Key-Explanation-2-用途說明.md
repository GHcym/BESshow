# 步驟 2：用途說明

## 🎯 AWS Access Key ID 的用途

### 主要用途
1. **AWS CLI 存取**：讓命令列工具能夠呼叫 AWS API
2. **SDK 開發**：程式碼中使用 AWS 服務
3. **第三方工具**：其他工具存取 AWS 資源
4. **自動化腳本**：批次處理和自動化任務

### 使用場景

#### AWS CLI
```bash
# 配置後可以執行
aws ec2 describe-instances
aws s3 ls
aws lambda list-functions
```

#### 程式開發
```python
# Python 範例
import boto3
client = boto3.client('ec2')
response = client.describe_instances()
```

#### 自動化部署
```bash
# CI/CD 管道中使用
aws s3 sync ./build s3://my-website
aws ecs update-service --service my-app
```

### 權限控制
- Access Key 繼承建立它的 IAM 用戶權限
- 可以透過 IAM 政策精確控制存取權限
- 支援最小權限原則

### 替代方案
1. **IAM Roles**：EC2 實例、Lambda 函數使用
2. **AWS SSO**：企業單一登入
3. **臨時憑證**：STS 服務產生的短期憑證
4. **AWS CLI SSO**：透過瀏覽器登入