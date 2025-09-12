# 步驟 3：常用連接埠設定

## 🔌 常見服務連接埠對照表

### Web 服務
| 服務 | 連接埠 | 協定 | 用途 |
|------|--------|------|------|
| HTTP | 80 | TCP | 網頁服務 |
| HTTPS | 443 | TCP | 安全網頁服務 |
| HTTP Alt | 8080 | TCP | 替代 HTTP |
| HTTPS Alt | 8443 | TCP | 替代 HTTPS |

### 遠端存取
| 服務 | 連接埠 | 協定 | 用途 |
|------|--------|------|------|
| SSH | 22 | TCP | Linux 遠端登入 |
| RDP | 3389 | TCP | Windows 遠端桌面 |
| Telnet | 23 | TCP | 不安全遠端登入 |

### 資料庫
| 服務 | 連接埠 | 協定 | 用途 |
|------|--------|------|------|
| MySQL | 3306 | TCP | MySQL 資料庫 |
| PostgreSQL | 5432 | TCP | PostgreSQL 資料庫 |
| MongoDB | 27017 | TCP | MongoDB 資料庫 |
| Redis | 6379 | TCP | Redis 快取 |

### 應用服務
| 服務 | 連接埠 | 協定 | 用途 |
|------|--------|------|------|
| Django | 8000 | TCP | Django 開發伺服器 |
| Flask | 5000 | TCP | Flask 開發伺服器 |
| Node.js | 3000 | TCP | Node.js 應用 |
| Docker | 2376 | TCP | Docker API |

## 📋 快速設定範本

### 基本 Web 伺服器
```bash
# SSH + HTTP + HTTPS
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 22 --cidr YOUR_IP/32
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 443 --cidr 0.0.0.0/0
```

### 開發環境
```bash
# SSH + 開發伺服器連接埠
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 22 --cidr YOUR_IP/32
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 8000 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 3000 --cidr 0.0.0.0/0
```

### 資料庫伺服器
```bash
# SSH + MySQL (僅限特定 IP)
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 22 --cidr YOUR_IP/32
aws ec2 authorize-security-group-ingress --group-id sg-xxx --protocol tcp --port 3306 --cidr YOUR_APP_SERVER_IP/32
```