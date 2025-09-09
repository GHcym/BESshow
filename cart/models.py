from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="使用者"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    def __str__(self):
        return f"{self.user.username} 的購物車"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = "購物車"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="購物車"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="燈種"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "購物車項目"
        verbose_name_plural = "購物車項目"
        unique_together = ('cart', 'product')