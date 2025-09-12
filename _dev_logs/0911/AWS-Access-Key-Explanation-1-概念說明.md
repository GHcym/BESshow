# 步驟 1：AWS Access Key ID 概念說明

## 🔑 什麼是 AWS Access Key ID

### 基本定義
**AWS Access Key ID** 是 AWS 身份驗證系統的一部分，用於識別 API 請求的發送者。

### 組成部分
AWS 憑證由兩部分組成：
1. **Access Key ID**：公開的識別碼（類似用戶名）
2. **Secret Access Key**：私密的密鑰（類似密碼）

### 格式範例
```
Access Key ID: AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### 類比說明
- **Access Key ID** = 銀行帳號（可以公開）
- **Secret Access Key** = 密碼（絕對保密）
- 兩者必須配對使用才能存取 AWS 服務

### 特徵
- **長度**：20 個字元
- **格式**：以 `AKIA` 開頭（一般用戶）或 `ASIA`（臨時憑證）
- **唯一性**：每個 Access Key ID 都是唯一的
- **可見性**：可以在 AWS Console 中查看（但 Secret Key 只能在建立時看到一次）