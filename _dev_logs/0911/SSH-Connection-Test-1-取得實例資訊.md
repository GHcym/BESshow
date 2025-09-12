# 步驟 1：取得實例資訊

## 具體操作指令
```bash
aws ec2 describe-instances --instance-ids i-07f5692f52fb7d948 \
  --query 'Reservations[0].Instances[0].{State:State.Name,PublicIP:PublicIpAddress,PrivateIP:PrivateIpAddress,KeyName:KeyName}' \
  --output table
```

## 輸出結果與說明
```
---------------------------------------------------------
|                   DescribeInstances                   |
+-----------+---------------+----------------+----------+
|  KeyName  |   PrivateIP   |   PublicIP     |  State   |
+-----------+---------------+----------------+----------+
|  bes-ec2-1|  172.31.35.9  |  43.213.18.62  |  running |
+-----------+---------------+----------------+----------+
```

## 實例資訊總結
- **狀態**：running ✅
- **公有 IP**：43.213.18.62
- **私有 IP**：172.31.35.9
- **金鑰對**：bes-ec2-1

## 分析
- 實例正在運行，這是好消息
- 有公有 IP 地址
- 使用金鑰對 bes-ec2-1 進行 SSH 驗證