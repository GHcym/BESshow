# 步驟 4：基本測試

## 具體操作指令
```bash
# 測試 help 功能
aws help | head -10

# 測試需要憑證的指令（預期失敗）
aws sts get-caller-identity --no-cli-pager 2>&1 || echo "Expected: No credentials configured"
```

## 輸入參數與說明
- `aws help`：顯示 AWS CLI 說明文件
- `aws sts get-caller-identity`：測試身份驗證（需要憑證）
- `--no-cli-pager`：不使用分頁器顯示輸出

## 輸出結果與說明
1. **Help 功能測試**：
   - 成功顯示 AWS CLI 說明文件開頭
   - 確認 CLI 基本功能正常

2. **憑證測試**：
   - 輸出：`Unable to locate credentials. You can configure credentials by running "aws configure".`
   - 狀態：符合預期（未配置憑證時的正常行為）
   - 說明：AWS CLI 功能正常，但需要配置憑證才能執行需要身份驗證的操作