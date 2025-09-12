# 步驟 2：連接埠測試

## 具體操作指令
```bash
# 方法 1：使用 bash TCP 測試
timeout 10 bash -c 'echo > /dev/tcp/43.213.18.62/22'

# 方法 2：使用 nc 測試
nc -zv -w5 43.213.18.62 22
```

## 輸出結果與說明
1. **Bash TCP 測試**：
   - 結果：`SSH port 22 is closed or filtered`
   - 狀態：失敗

2. **nc 測試**：
   - 結果：`nc: connect to 43.213.18.62 port 22 (tcp) timed out`
   - 狀態：連線逾時

## 分析結果
- ❌ **SSH 連接埠 22 無法連通**
- 可能原因：
  1. 安全群組未開放連接埠 22
  2. 網路 ACL 阻擋流量
  3. 實例內部防火牆阻擋
  4. SSH 服務未啟動

## 初步診斷
雖然實例狀態為 running，但 SSH 連接埠無法存取，需要檢查安全群組設定。