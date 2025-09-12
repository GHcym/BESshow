# AWS-Deploy 步驟 2：EC2設定

## 具體操作指令
建立 EC2 實例與安全群組配置，為 BESshow 應用程式準備運行環境

## 輸入參數與說明
- 區域：ap-east-1 (香港)
- 實例類型：t3.micro (測試階段適用)
- AMI：Ubuntu 22.04 LTS
- 安全群組：開放 SSH(22)、HTTP(80)、HTTPS(443)、Django(8000) 端口

## 執行步驟

### 2.1 建立安全群組
```bash
$ aws ec2 create-security-group --group-name besshow-sg --description "Security group for BESshow application" --region ap-east-1
{
    "GroupId": "sg-06cbc7c3891ca5d8c",
    "SecurityGroupArn": "arn:aws:ec2:ap-east-1:371293080356:security-group/sg-06cbc7c3891ca5d8c"
}
```
✅ 安全群組建立成功
- 群組 ID：sg-06cbc7c3891ca5d8c
- 名稱：besshow-sg

### 2.2 配置安全群組規則
```bash
$ aws ec2 authorize-security-group-ingress --group-id sg-06cbc7c3891ca5d8c --protocol tcp --port 22 --cidr 0.0.0.0/0 --region ap-east-1
# SSH 連接埠 22 開放成功

$ aws ec2 authorize-security-group-ingress --group-id sg-06cbc7c3891ca5d8c --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ap-east-1
# HTTP 連接埠 80 開放成功

$ aws ec2 authorize-security-group-ingress --group-id sg-06cbc7c3891ca5d8c --protocol tcp --port 8000 --cidr 0.0.0.0/0 --region ap-east-1
# Django 開發埠 8000 開放成功
```
✅ 安全群組規則配置完成
- SSH (22)、HTTP (80)、Django (8000) 連接埠已開放

### 2.3 建立 Key Pair
```bash
$ aws ec2 describe-key-pairs --region ap-east-1
{
    "KeyPairs": []
}

$ aws ec2 create-key-pair --key-name besshow-key --query 'KeyMaterial' --output text --region ap-east-1 > /home/ksu/bess/besshow/.key/besshow-key.pem
$ chmod 400 /home/ksu/bess/besshow/.key/besshow-key.pem
```
✅ SSH 金鑰對建立成功
- 金鑰名稱：besshow-key
- 私鑰檔案：/home/ksu/bess/besshow/.key/besshow-key.pem

### 2.4 建立 EC2 實例
```bash
$ aws ec2 run-instances --image-id ami-0dd0166907823fe98 --count 1 --instance-type t3.micro --key-name besshow-key --security-group-ids sg-06cbc7c3891ca5d8c --region ap-east-1 --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=besshow-server}]'
# 實例建立成功，實例 ID: i-007829cf4b3de6c5e
```
✅ EC2 實例建立成功
- 實例 ID：i-007829cf4b3de6c5e
- AMI：Ubuntu 22.04 LTS (ami-0dd0166907823fe98)
- 實例類型：t3.micro

### 2.5 獲取實例資訊
```bash
$ aws ec2 describe-instances --instance-ids i-007829cf4b3de6c5e --query 'Reservations[0].Instances[0].[State.Name,PublicIpAddress,PublicDnsName]' --output table --region ap-east-1
-------------------------------------------------------
|                  DescribeInstances                  |
+-----------------------------------------------------+
|  running                                            |
|  43.198.12.223                                      |
|  ec2-43-198-12-223.ap-east-1.compute.amazonaws.com  |
+-----------------------------------------------------+
```
✅ 實例狀態確認
- 狀態：running
- 公共 IP：43.198.12.223
- 公共 DNS：ec2-43-198-12-223.ap-east-1.compute.amazonaws.com

## 輸出結果與說明
- EC2 實例已成功建立並運行
- 安全群組已配置必要的連接埠
- SSH 金鑰對已建立並儲存
- 下一步：可以開始準備 Docker 配置檔案

📝 **重要資訊記錄**：
- 實例 ID：i-007829cf4b3de6c5e
- 公共 IP：43.198.12.223
- SSH 連線指令：`ssh -i /home/ksu/bess/besshow/.key/besshow-key.pem ubuntu@43.198.12.223`