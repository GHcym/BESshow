# 步驟 3：安全群組檢查

## 具體操作指令
由於 AWS CLI 未配置憑證，無法直接查詢安全群組設定。

## 建議檢查項目
需要在 AWS Console 或配置 AWS CLI 後檢查：

### 必要的安全群組規則
1. **SSH 存取 (連接埠 22)**：
   ```
   Type: SSH
   Protocol: TCP
   Port Range: 22
   Source: 0.0.0.0/0 或特定 IP
   ```

2. **HTTP 存取 (連接埠 80)**：
   ```
   Type: HTTP
   Protocol: TCP
   Port Range: 80
   Source: 0.0.0.0/0
   ```

3. **HTTPS 存取 (連接埠 443)**：
   ```
   Type: HTTPS
   Protocol: TCP
   Port Range: 443
   Source: 0.0.0.0/0
   ```

## 常見問題
- 安全群組未開放必要連接埠
- 來源 IP 限制過嚴
- 出站規則被限制