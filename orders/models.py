import uuid
from django.db import models
from django.conf import settings
from products.models import Product

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

    class Meta:
        verbose_name = "訂單項目"
        verbose_name_plural = "訂單項目"

    def __str__(self):
        return str(self.id)

    @property
    def subtotal(self):
        return self.quantity * self.price