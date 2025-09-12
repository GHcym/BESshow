# AWS-EC2-Staging-Deploy - 步驟1：AWS環境準備

## 具體操作指令
設定 AWS 帳單告警和選擇部署區域

## 輸入參數與說明
- 登入 AWS Console
- 選擇區域：ap-northeast-1 (東京)
- 設定預算告警：$10 USD
- 確認免費額度狀態

## 操作步驟

### 1.1 登入 AWS Console
1. 前往 https://aws.amazon.com/console/
2. 使用您的 AWS 帳號登入
3. 確認右上角區域選擇為 **Asia Pacific (Tokyo) ap-northeast-1**

### 1.2 設定帳單告警
1. 前往 **Billing and Cost Management**
2. 點選 **Budgets** > **Create budget**
3. 選擇 **Cost budget**
4. 設定參數：
   - Budget name: `BESshow-Monthly-Budget`
   - Budget amount: `$10.00`
   - Time period: `Monthly`
5. 設定告警：
   - Alert threshold: `80%` ($8.00)
   - Email: 您的 Email 地址
6. 點選 **Create budget**

### 1.3 檢查免費額度
1. 前往 **Billing** > **Free Tier**
2. 確認以下項目可用：
   - EC2 t3.micro: 750 hours/month
   - EBS General Purpose (gp3): 30 GB/month
   - Data Transfer Out: 15 GB/month

### 1.4 準備 Key Pair（如果沒有）
1. 前往 **EC2** > **Key Pairs**
2. 點選 **Create key pair**
3. 設定：
   - Name: `besshow-key`
   - Key pair type: `RSA`
   - Private key file format: `.pem`
4. 下載並妥善保存 `.pem` 檔案

## 輸出結果與說明

### 完成檢查項目
- ✅ AWS Console 登入成功
- ✅ 區域設定為 ap-northeast-1 (東京)
- ✅ 帳單告警設定完成 ($10 預算)
- ✅ 免費額度確認可用
- ✅ Key Pair 準備完成

### 重要資訊記錄
- **區域**：ap-northeast-1 (Asia Pacific - Tokyo)
- **預算告警**：$10 USD (80% = $8 告警)
- **Key Pair 名稱**：besshow-key
- **預期延遲**：30-50ms (台北到東京)

### 下一步準備
- EC2 實例規格：t3.micro
- 作業系統：Ubuntu 22.04 LTS
- 儲存空間：30GB gp3 (免費額度內)
- 安全群組：SSH, HTTP, Custom TCP 8000