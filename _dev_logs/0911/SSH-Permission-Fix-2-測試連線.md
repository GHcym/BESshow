# 步驟 2：測試連線

## 具體操作指令
```bash
ssh -v -i bes-ec2-1.pem -o ConnectTimeout=10 ec2-user@43.213.18.62
```

## 輸出結果與說明

### 連線建立 ✅
```
debug1: Connection established.
debug1: identity file bes-ec2-1.pem type 3
debug1: Authenticating to 43.213.18.62:22 as 'ec2-user'
```

### 金鑰資訊 ✅
```
debug1: Will attempt key: bes-ec2-1.pem ED25519 SHA256:SsaWwKJuXzb39UcO6GtlXrFgF/xMr39gsiyoozAUmKs explicit
debug1: Offering public key: bes-ec2-1.pem ED25519 SHA256:SsaWwKJuXzb39UcO6GtlXrFgF/xMr39gsiyoozAUmKs explicit
```

### 驗證失敗 ❌
```
debug1: Authentications that can continue: publickey
debug1: No more authentication methods to try.
ec2-user@43.213.18.62: Permission denied (publickey).
```

## 分析結果

### 正常的部分
- ✅ **網路連線**：成功建立連線
- ✅ **SSH 服務**：伺服器正常回應
- ✅ **私鑰格式**：ED25519 金鑰正確載入
- ✅ **金鑰指紋**：SHA256:SsaWwKJuXzb39UcO6GtlXrFgF/xMr39gsiyoozAUmKs

### 問題所在
- ❌ **公鑰驗證失敗**：伺服器拒絕了提供的公鑰
- 可能原因：
  1. 實例上沒有對應的公鑰
  2. 用戶名 'ec2-user' 不正確
  3. 金鑰對不匹配

## 診斷結論
- SSH 連線和金鑰檔案都正常
- 問題在於伺服器端的公鑰驗證
- 需要檢查用戶名或金鑰對匹配性