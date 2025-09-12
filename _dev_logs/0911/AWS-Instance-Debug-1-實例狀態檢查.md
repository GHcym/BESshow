# 步驟 1: 實例狀態檢查

## 具體操作指令
檢查 EC2 實例 i-07f5692f52fb7d948 的基本狀態和健康檢查

## 輸入參數與說明
- 實例 ID: i-07f5692f52fb7d948
- 需要檢查的項目: 實例狀態、IP 地址、VPC 配置、安全群組

## 執行結果與說明
**問題**: 本地環境未安裝 AWS CLI 工具

**需要的診斷指令**:
```bash
# 檢查實例狀態
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948

# 檢查實例健康狀態
aws ec2 describe-instance-status --instance-ids i-07f5692f52fb7d948

# 檢查系統日誌
aws ec2 get-console-output --instance-id i-07f5692f52fb7d948
```

**替代方案**: 使用 AWS 管理控制台進行檢查
1. 登入 AWS Console
2. 進入 EC2 服務
3. 搜尋實例 i-07f5692f52fb7d948
4. 檢查實例狀態、網路設定、安全群組