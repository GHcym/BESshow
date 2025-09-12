# 步驟 1：AWS Console 操作方法

## 🖥️ AWS Console 開放連接埠步驟

### 1. 登入 AWS Console
- 前往 [AWS Console](https://console.aws.amazon.com)
- 登入您的 AWS 帳戶

### 2. 進入 EC2 服務
- 搜尋並點擊 "EC2"
- 或直接前往 EC2 Dashboard

### 3. 找到安全群組
**方法一：透過實例**
1. 點擊 "Instances"
2. 選擇目標實例 (i-07f5692f52fb7d948)
3. 點擊 "Security" 標籤
4. 點擊安全群組名稱

**方法二：直接查找**
1. 左側選單點擊 "Security Groups"
2. 搜尋或找到目標安全群組

### 4. 編輯入站規則
1. 選擇安全群組
2. 點擊 "Inbound rules" 標籤
3. 點擊 "Edit inbound rules"

### 5. 新增規則
1. 點擊 "Add rule"
2. 設定規則：
   - **Type**: 選擇服務類型 (SSH, HTTP, HTTPS, Custom TCP)
   - **Port range**: 連接埠號碼
   - **Source**: 來源 IP 範圍
3. 點擊 "Save rules"

## 📝 常見設定範例

### SSH 存取 (連接埠 22)
```
Type: SSH
Protocol: TCP
Port Range: 22
Source: 0.0.0.0/0 (所有 IP) 或 您的 IP
```

### HTTP 存取 (連接埠 80)
```
Type: HTTP
Protocol: TCP
Port Range: 80
Source: 0.0.0.0/0
```

### HTTPS 存取 (連接埠 443)
```
Type: HTTPS
Protocol: TCP
Port Range: 443
Source: 0.0.0.0/0
```