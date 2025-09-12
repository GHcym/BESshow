# Order-History-Query - 步驟3：實作後端邏輯

## 具體操作指令
建立訂單查詢視圖和過濾功能

## 輸入參數與說明
- 修改 orders/views.py：加入 order_history 視圖
- 修改 orders/urls.py：加入歷史訂單路由
- 使用 Paginator 進行分頁處理

## 輸出結果與說明

### 視圖實作
```python
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/history.html', {'page_obj': page_obj})
```

### 功能特點
- 使用 `@login_required` 確保只有登入用戶可存取
- 過濾當前用戶的訂單：`filter(user=request.user)`
- 使用 `prefetch_related('items__product')` 優化查詢效能
- 每頁顯示10筆訂單記錄
- 支援分頁導航

### 路由配置
- URL：`/orders/history/`
- 名稱：`orders:order_history`

### 已完成項目
- ✅ 後端視圖邏輯
- ✅ URL 路由配置
- ✅ 查詢效能優化
- ✅ 分頁功能