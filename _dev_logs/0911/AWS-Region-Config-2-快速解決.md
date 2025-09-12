# 步驟 2：快速解決方案

## ⚡ 立即解決方法

### 方法 1：在指令中指定區域
```bash
# 原指令
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948

# 加上 --region 參數
aws ec2 describe-instances --region ap-northeast-1 --instance-ids i-07f5692f52fb7d948
```

### 方法 2：設定環境變數
```bash
# 設定區域環境變數
export AWS_DEFAULT_REGION=ap-northeast-1

# 執行指令（不需要 --region）
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948
```

### 方法 3：一次性設定
```bash
# 僅設定區域（不設定憑證）
aws configure set region ap-northeast-1
```

## 🌏 常用 AWS 區域代碼

### 亞太地區
- `ap-northeast-1` - 東京
- `ap-northeast-2` - 首爾  
- `ap-southeast-1` - 新加坡
- `ap-southeast-2` - 雪梨

### 美國地區
- `us-east-1` - 維吉尼亞北部
- `us-west-2` - 奧勒岡

### 歐洲地區
- `eu-west-1` - 愛爾蘭
- `eu-central-1` - 法蘭克福

## 💡 如何選擇區域
1. **檢查 EC2 實例位置**：在 AWS Console 查看實例所在區域
2. **就近原則**：選擇地理位置最近的區域
3. **服務可用性**：確認所需服務在該區域可用