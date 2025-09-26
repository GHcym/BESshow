# 燈牆管理功能設計方案

## 概述

新增燈牆管理功能，用於管理多個EPD播放器的配置。每面燈牆由12個EPD Player組成，每個Player控制12個EPD設備。

## 需求分析

### 功能需求
1. **燈牆設定頁面**：管理12個EPD Player的序號輸入、修改、啟用/停用
2. **多頁面管理**：支援多個燈牆配置的建立、刪除、啟用/停用
3. **狀態查看**：根據序號查看播放器狀態 `/epd/player/序號/`
4. **離線支援**：本地儲存配置，支援網路斷線時的操作
5. **同步功能**：提供上傳更新、下載同步功能

### 技術需求
- 與現有EPD API整合
- 超級管理員權限控制
- 本地資料庫儲存
- 響應式管理介面

## 架構設計

### 資料模型

#### LanternWall (燈牆)
```python
class LanternWall(models.Model):
    name = models.CharField(max_length=100, verbose_name="燈牆名稱")
    description = models.TextField(blank=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "燈牆"
        verbose_name_plural = "燈牆管理"
```

#### LanternPlayer (燈牆播放器)
```python
class LanternPlayer(models.Model):
    wall = models.ForeignKey(LanternWall, on_delete=models.CASCADE, related_name='players')
    position = models.PositiveIntegerField(verbose_name="位置 (1-12)")
    serial_number = models.CharField(max_length=50, blank=True, verbose_name="序號")
    is_enabled = models.BooleanField(default=True, verbose_name="啟用狀態")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "燈牆播放器"
        verbose_name_plural = "燈牆播放器"
        unique_together = ['wall', 'position']
        ordering = ['position']
```

### URL設計

```
/epd/wall/                    # 燈牆列表
/epd/wall/create/             # 新增燈牆
/epd/wall/<wall_id>/          # 燈牆設定頁面
/epd/wall/<wall_id>/edit/     # 編輯燈牆
/epd/wall/<wall_id>/delete/   # 刪除燈牆
/epd/player/<serialnum>/      # 根據序號查看狀態 (新路由)
/epd/wall/sync/upload/        # 上傳同步
/epd/wall/sync/download/      # 下載同步
```

### 視圖設計

#### 主要視圖
1. **LanternWallListView** - 燈牆列表頁面
2. **LanternWallCreateView** - 新增燈牆
3. **LanternWallUpdateView** - 編輯燈牆設定
4. **LanternWallDeleteView** - 刪除燈牆
5. **PlayerStatusBySerialView** - 根據序號查看狀態
6. **SyncUploadView** - 上傳同步
7. **SyncDownloadView** - 下載同步

#### 表單設計
- **LanternWallForm** - 燈牆基本資訊表單
- **LanternPlayerFormSet** - 12個播放器設定表單集

### 模板設計

#### 主要模板
- `epd_management/lantern_wall_list.html` - 燈牆列表
- `epd_management/lantern_wall_form.html` - 燈牆設定表單
- `epd_management/player_status_by_serial.html` - 序號狀態查看

### API整合

#### 與現有EPD API的整合
- 使用 `EPDAPIClient` 獲取播放器資訊
- 根據本地序號查詢外部API狀態
- 支援批量操作

#### 同步功能
- **上傳同步**：將本地配置同步到外部API
- **下載同步**：從外部API同步最新狀態到本地

## 實作步驟

1. 建立資料模型和遷移
2. 建立表單和表單集
3. 實作視圖邏輯
4. 設計模板介面
5. 整合API功能
6. 實作同步機制
7. 測試和驗證

## 安全考量

- 超級管理員權限控制
- 輸入驗證和清理
- API調用錯誤處理
- 離線操作的安全性

## 效能考量

- 批量API調用優化
- 資料庫查詢優化
- 快取機制
- 非同步處理

## 測試策略

- 單元測試：模型和表單
- 整合測試：視圖和API整合
- 功能測試：完整工作流程
- 壓力測試：多燈牆操作