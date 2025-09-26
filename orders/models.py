import uuid
from django.db import models
from django.conf import settings
from products.models import Product
from epd_management.models import LanternPlayer

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name="使用者"
    )
    # Store a snapshot of user details at the time of order
    full_name = models.CharField(max_length=255, verbose_name="姓名")
    email = models.EmailField(verbose_name="電子郵件")
    phone_number = models.CharField(max_length=20, verbose_name="手機號碼")
    address = models.CharField(max_length=255, verbose_name="完整地址")

    total_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="總金額")
    paid = models.BooleanField(default=False, verbose_name="是否已付款")
    order_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="訂單識別碼")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    # 點燈處理相關欄位
    PROCESSING_STATUS_CHOICES = [
        ('pending', '未處理'),
        ('processing', '處理中'),
        ('completed', '已完成'),
        ('failed', '失敗'),
    ]
    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default='pending',
        verbose_name="處理狀態"
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_orders',
        verbose_name="處理人員"
    )
    processing_started_at = models.DateTimeField(null=True, blank=True, verbose_name="處理開始時間")
    processing_completed_at = models.DateTimeField(null=True, blank=True, verbose_name="處理完成時間")
    processing_notes = models.TextField(null=True, blank=True, verbose_name="處理備註")

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def __str__(self):
        return f"訂單 {self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="訂單")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="燈種")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")

    # 生成的圖片欄位
    generated_image = models.ImageField(upload_to='generated_lanterns/', null=True, blank=True, verbose_name="生成的圖片")
    image_generated_at = models.DateTimeField(null=True, blank=True, verbose_name="圖片生成時間")

    class Meta:
        verbose_name = "訂單項目"
        verbose_name_plural = "訂單項目"

    def __str__(self):
        return str(self.id)

    @property
    def subtotal(self):
        return self.quantity * self.price


class OrderItemPlayerAssignment(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name="訂單項目")
    player = models.ForeignKey(LanternPlayer, on_delete=models.CASCADE, verbose_name="播放器")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="配對時間")
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="配對人員"
    )

    # 上傳狀態欄位
    UPLOAD_STATUS_CHOICES = [
        ('pending', '待上傳'),
        ('uploading', '上傳中'),
        ('completed', '已完成'),
        ('failed', '失敗'),
    ]
    upload_status = models.CharField(
        max_length=20,
        choices=UPLOAD_STATUS_CHOICES,
        default='pending',
        verbose_name="上傳狀態"
    )
    epd_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="EPD 設備 ID")
    uploaded_at = models.DateTimeField(null=True, blank=True, verbose_name="上傳完成時間")
    upload_error = models.TextField(null=True, blank=True, verbose_name="上傳錯誤訊息")

    class Meta:
        unique_together = ('order_item', 'epd_id')
        verbose_name = "訂單項目播放器配對"
        verbose_name_plural = "訂單項目播放器配對"

    def __str__(self):
        return f"{self.order_item} - {self.player}"