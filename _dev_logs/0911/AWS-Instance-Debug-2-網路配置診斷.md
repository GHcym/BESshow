# 步驟 2: 網路配置診斷

## 具體操作指令
在沒有 AWS CLI 的情況下，進行基本網路連通性測試

## 輸入參數與說明
- 實例 ID: i-07f5692f52fb7d948
- 需要用戶提供: 實例的公共 IP 地址

## 執行結果與說明

**需要用戶提供的資訊**:
1. 實例的公共 IP 地址
2. 預期的 SSH 連接埠 (通常是 22)
3. 使用的 SSH 金鑰檔案路徑

**可執行的基本測試**:
```bash
# 測試網路連通性 (需要 IP 地址)
ping -c 4 <PUBLIC_IP>

# 測試 SSH 埠連通性
telnet <PUBLIC_IP> 22
# 或使用 nc
nc -zv <PUBLIC_IP> 22

# 測試 SSH 連線 (需要金鑰檔案)
ssh -i <KEY_FILE> -v ec2-user@<PUBLIC_IP>
```