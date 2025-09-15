# Django 專家模組

## 專業領域
- **Models**: 資料模型設計與 ORM 操作
- **Views**: 視圖邏輯與請求處理
- **Templates**: 模板系統與前端整合
- **Forms**: 表單處理與驗證
- **Admin**: 後台管理系統
- **Authentication**: 使用者認證與授權
- **Testing**: 單元測試與整合測試

## 技術重點

### Models 最佳實踐
```python
# 良好的 Model 設計範例
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class User(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
```

### Views 設計模式
- **Function-Based Views**: 簡單邏輯
- **Class-Based Views**: 複雜功能
- **Generic Views**: 標準 CRUD 操作
- **API Views**: REST API 端點

### 安全考量
- CSRF 保護
- SQL 注入防護
- XSS 防護
- 使用者輸入驗證
- 權限控制

## 常見問題解決
1. **N+1 查詢問題**: 使用 `select_related()` 和 `prefetch_related()`
2. **遷移衝突**: 合併遷移檔案
3. **靜態檔案**: 正確配置 STATIC_URL 和 MEDIA_URL
4. **時區處理**: 使用 UTC 時間

## 開發工具
- Django Debug Toolbar
- Django Extensions
- pytest-django
- factory_boy