# AWS-Deploy 步驟 1：環境準備

## 具體操作指令
檢查 AWS CLI 配置與權限狀態

## 輸入參數與說明
- 無需額外參數
- 檢查本機 AWS CLI 安裝與配置狀態

## 執行步驟

### 1.1 檢查 AWS CLI 安裝狀態
```bash
$ aws --version
aws-cli/2.30.0 Python/3.13.7 Linux/6.6.87.2-microsoft-standard-WSL2 exec-env/AmazonQ-For-IDE Version/1.94.0 exe/x86_64.ubuntu.24
```
✅ AWS CLI 版本：2.30.0 (已安裝)

### 1.2 檢查 AWS 配置狀態
```bash
$ aws configure list
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************YUPC shared-credentials-file    
secret_key     ****************TDIZ shared-credentials-file    
    region                ap-east-2      config-file    ~/.aws/config
```
✅ Access Key：已配置 (****************YUPC)
✅ Secret Key：已配置
✅ 預設區域：ap-east-2

### 1.3 驗證 AWS 連線與權限
```bash
$ aws sts get-caller-identity
{
    "UserId": "AIDAVM4WKZMSANT7J2O2G",
    "Account": "371293080356",
    "Arn": "arn:aws:iam::371293080356:user/KANG"
}
```
✅ 身份驗證：成功
- 用戶：KANG
- 帳戶 ID：371293080356
- ARN：arn:aws:iam::371293080356:user/KANG

```bash
$ aws ec2 describe-regions --region ap-east-1 --output table
# (輸出顯示可存取多個區域，包含 ap-east-1, ap-east-2 等)
```
✅ EC2 權限：已驗證
- 可存取 ap-east-1, ap-east-2 等區域
- 建議使用 ap-east-1 (香港) 進行部署

## 輸出結果與說明
- AWS CLI 環境已完整配置
- 具備 EC2 操作權限
- 建議部署區域：ap-east-1 (延遲較低)