# 步驟 1：實例狀態檢查

## 具體操作指令
```bash
aws ec2 describe-instances --region ap-northeast-1 --instance-ids i-07f5692f52fb7d948
```

## 輸入參數與說明
- Instance ID: i-07f5692f52fb7d948
- Region: ap-northeast-1 (推測)

## 輸出結果與說明
- 狀態：失敗 (exit code: 253)
- 錯誤：`Unable to locate credentials`
- 說明：AWS CLI 未配置憑證，無法直接查詢 AWS API

## 替代方案
改用網路層面的診斷方法進行問題排查