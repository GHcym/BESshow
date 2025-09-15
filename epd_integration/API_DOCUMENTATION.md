# BES EPD API 完整說明文件

## 概述

BES (Bless Electronic Paper Display) API 是一個 RESTful API，提供電子紙顯示系統的後端服務。

**API 基本資訊：**
- **基礎 URL**: `http://43.213.2.34/api`
- **API 版本**: 1.0.0
- **認證方式**: Token-based Authentication
- **文件地址**: `http://43.213.2.34/api/redoc/`

## 認證系統

### Token 認證
所有 API 請求都需要在 Header 中包含認證 Token：

```
Authorization: Token your-token-here
```

### 取得 Token
**端點**: `POST /api/user/token/`

**請求參數**:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

**回應**:
```json
{
  "token": "7d78d4d0dca2043feced803d0a6a8c774a6fd908"
}
```

## 核心功能模組

### 1. 使用者管理 (User Management)

#### 建立使用者
- **端點**: `POST /api/user/create/`
- **功能**: 註冊新使用者
- **參數**: email, password, name

#### 取得使用者資訊
- **端點**: `GET /api/user/me/`
- **功能**: 取得當前認證使用者資訊

### 2. 播放器管理 (Player Management)

播放器是電子紙系統的核心設備，每個播放器可以管理多個 EPD 設備。

#### 建立播放器
- **端點**: `POST /api/player/`
- **功能**: 註冊新的播放器設備

**請求參數**:
```json
{
  "serialnum": "TEMPLE_001"
}
```

**回應範例**:
```json
{
  "id": 17,
  "serialnum": "TEMPLE_001",
  "version": "1.0.0",
  "indicator": "RED",
  "location": "Taipei",
  "ip": "192.168.51.122",
  "mac": "2C:BC:BB:26:25:E8",
  "heartbeat_interval": 5,
  "created_time": "2025-01-13T07:37:26.398511Z",
  "last_sync": "2025-01-13T05:15:18.799129Z",
  "online_status": false,
  "enabled": true,
  "epds": []
}
```

#### 列出播放器
- **端點**: `GET /api/player/players/`
- **功能**: 取得所有播放器列表
- **查詢參數**: `serialnum` (可選，按序號過濾)

#### 取得特定播放器
- **端點**: `GET /api/player/{id}/`
- **功能**: 取得指定播放器的詳細資訊

#### 更新播放器
- **端點**: `PUT /api/player/{id}/` 或 `PATCH /api/player/{id}/`
- **功能**: 更新播放器資訊

#### 刪除播放器
- **端點**: `DELETE /api/player/{id}/`
- **功能**: 刪除播放器

### 3. EPD 設備管理 (EPD Management)

EPD (Electronic Paper Display) 是實際的電子紙顯示設備。

#### 建立 EPD 設備
- **端點**: `POST /api/player/{player_id}/epd/`
- **功能**: 為指定播放器建立 EPD 設備

**請求參數**:
```json
{
  "order": 1
}
```

**回應範例**:
```json
{
  "id": 262,
  "order": 1,
  "created_time": "2025-01-13T07:37:43.747101Z",
  "updated": false,
  "update_time": "2025-01-13T07:42:39.977530Z",
  "images": []
}
```

#### 列出 EPD 設備
- **端點**: `GET /api/player/epds/`
- **功能**: 取得所有 EPD 設備列表
- **查詢參數**: `epd_id` (可選，按 EPD ID 過濾)

#### 取得特定 EPD
- **端點**: `GET /api/player/epd/{epd_id}/`
- **功能**: 取得指定 EPD 設備的詳細資訊

#### 更新 EPD 設備
- **端點**: `PUT /api/player/epd/{epd_id}/` 或 `PATCH /api/player/epd/{epd_id}/`
- **功能**: 更新 EPD 設備狀態

**常用更新參數**:
```json
{
  "order": 2,
  "updated": true
}
```

#### 刪除 EPD 設備
- **端點**: `DELETE /api/player/epd/{epd_id}/`
- **功能**: 刪除 EPD 設備

### 4. 圖片管理 (Image Management)

圖片是顯示在 EPD 設備上的內容。

#### 上傳圖片
- **端點**: `POST /api/player/epd/{epd_id}/image/`
- **功能**: 上傳圖片到指定 EPD 設備
- **內容類型**: `multipart/form-data`

**請求參數**:
```
upload_image: [圖片檔案]
```

**回應範例**:
```json
{
  "id": 192,
  "upload_image": "http://43.213.2.34/static/media/uploads/epd/CM2025091006/image.jpg",
  "four_color_image": "http://43.213.2.34/static/media/uploads/epd/CM2025091006/image_4color_data.gz",
  "converted_image": "http://43.213.2.34/static/media/uploads/epd/CM2025091006/image_converted.png",
  "created_time": "2025-01-13T07:38:52.864032Z",
  "update_time": "2025-01-13T07:38:52.864049Z"
}
```

#### 列出圖片
- **端點**: `GET /api/player/images/`
- **功能**: 取得所有圖片列表
- **查詢參數**: `id` (可選，按圖片 ID 過濾)

#### 取得特定圖片
- **端點**: `GET /api/player/image/{image_id}/`
- **功能**: 取得指定圖片的詳細資訊

#### 更新圖片
- **端點**: `PUT /api/player/image/{image_id}/` 或 `PATCH /api/player/image/{image_id}/`
- **功能**: 更新圖片資訊

#### 刪除圖片
- **端點**: `DELETE /api/player/image/{image_id}/`
- **功能**: 刪除圖片及相關檔案

## 資料模型說明

### 播放器 (Player)
```json
{
  "id": 17,                           // 播放器 ID
  "serialnum": "CM2025091006",        // 序號 (唯一)
  "version": "1.0.0",                 // 版本
  "indicator": "RED",                 // 指示燈狀態
  "location": "Taipei",               // 位置
  "ip": "192.168.51.122",            // IP 地址
  "mac": "2C:BC:BB:26:25:E8",        // MAC 地址
  "heartbeat_interval": 5,            // 心跳間隔 (秒)
  "created_time": "2025-01-13T07:37:26Z", // 建立時間
  "last_sync": "2025-01-13T05:15:18Z",    // 最後同步時間
  "online_status": false,             // 線上狀態
  "enabled": true,                    // 啟用狀態
  "epds": []                         // 關聯的 EPD 設備列表
}
```

### EPD 設備 (EPD)
```json
{
  "id": 262,                         // EPD ID
  "order": 1,                        // 顯示順序 (1-12)
  "created_time": "2025-01-13T07:37:43Z", // 建立時間
  "updated": false,                  // 是否需要同步
  "update_time": "2025-01-13T07:42:39Z",  // 更新時間
  "images": []                       // 關聯的圖片列表
}
```

### 圖片 (Image)
```json
{
  "id": 192,                         // 圖片 ID
  "upload_image": "http://...",      // 原始上傳圖片 URL
  "four_color_image": "http://...",  // 四色處理圖片 URL
  "converted_image": "http://...",   // 轉換後圖片 URL
  "created_time": "2025-01-13T07:38:52Z", // 建立時間
  "update_time": "2025-01-13T07:38:52Z"   // 更新時間
}
```

## 使用流程範例

### 1. 基本設定流程
```python
# 1. 認證
client = EPDAPIClient()
client.authenticate('your-email@example.com', 'your-password')

# 2. 建立播放器
player = client.create_player('TEMPLE_001')

# 3. 建立 EPD 設備
epd = client.create_epd(player.id, order=1)

# 4. 上傳圖片
with open('lantern_image.jpg', 'rb') as image_file:
    image = client.upload_image(epd.id, image_file)

# 5. 標記需要更新
client.update_epd(epd.id, updated=True)
```

### 2. 點燈流程整合
```python
def update_lantern_display(customer_name, prayer_text):
    """更新點燈顯示內容"""
    client = EPDAPIClient(token='your-token')
    
    # 取得可用的 EPD 設備
    epds = client.list_epds()
    available_epd = epds[0]  # 選擇第一個可用設備
    
    # 生成點燈圖片 (需要實作圖片生成邏輯)
    # image_path = generate_lantern_image(customer_name, prayer_text)
    
    # 上傳圖片
    # with open(image_path, 'rb') as image_file:
    #     client.upload_image(available_epd.id, image_file)
    
    # 標記需要更新
    client.update_epd(available_epd.id, updated=True)
```

## 錯誤處理

### 常見錯誤碼
- **401**: 認證失敗 - 檢查 Token 是否正確
- **404**: 資源不存在 - 檢查 ID 是否正確
- **400**: 資料驗證錯誤 - 檢查請求參數格式

### 錯誤回應格式
```json
{
  "detail": "錯誤描述",
  "code": "error_code"
}
```

## 最佳實踐

### 1. 認證管理
- 安全儲存 Token
- 定期更新 Token
- 使用環境變數管理認證資訊

### 2. 圖片上傳
- 支援格式：JPG, PNG
- 建議尺寸：根據 EPD 設備規格
- 檔案大小限制：建議 < 5MB

### 3. 設備管理
- 定期檢查設備狀態
- 合理設定 heartbeat_interval
- 監控 online_status

### 4. 效能優化
- 批次處理多個操作
- 使用適當的查詢參數過濾
- 避免頻繁的狀態更新

## 聯絡資訊

**API 支援**: ellis.cc.su@cymmetrik.com

---

*此文件基於 BES EPD API v1.0.0 生成*