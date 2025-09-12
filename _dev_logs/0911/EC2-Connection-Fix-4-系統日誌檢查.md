# 步驟 4：系統日誌檢查

## 具體操作指令
由於 AWS CLI 未配置憑證，無法直接查詢系統日誌。

## 建議檢查項目
需要在 AWS Console 中檢查：

### EC2 Console 檢查
1. **實例狀態**：
   - Instance State: running/stopped/terminated
   - Status Checks: System/Instance reachability

2. **系統日誌**：
   - Actions → Monitor and troubleshoot → Get system log
   - 查看開機過程是否有錯誤

3. **實例截圖**：
   - Actions → Monitor and troubleshoot → Get instance screenshot
   - 查看當前畫面狀態

### CloudWatch 日誌
- 檢查 CloudWatch Logs 中的系統日誌
- 查看應用程式日誌

## 常見問題指標
- 開機失敗
- 磁碟空間不足
- 記憶體不足
- 服務啟動失敗