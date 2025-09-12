# 步驟 3：永久設定

## 🔧 配置預設區域

### 執行的設定指令
```bash
aws configure set region ap-east-2
```

### 設定說明
- **區域**：ap-east-2 (香港)
- **效果**：所有 AWS CLI 指令將預設使用此區域
- **配置檔案**：`~/.aws/config`

### 其他設定方法

#### 方法 1：完整配置
```bash
aws configure
# 會提示輸入：
# AWS Access Key ID: (可留空)
# AWS Secret Access Key: (可留空)  
# Default region name: ap-east-2
# Default output format: json
```

#### 方法 2：環境變數
```bash
# 加入到 ~/.bashrc 或 ~/.zshrc
export AWS_DEFAULT_REGION=ap-east-2
```

#### 方法 3：直接編輯配置檔案
```bash
# 編輯 ~/.aws/config
[default]
region = ap-east-2
output = json
```

### 驗證設定
```bash
aws configure get region
# 應該輸出：ap-east-2
```