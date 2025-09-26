from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="燈種名稱")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="燈種圖片")
    prayer_text = models.TextField(blank=True, verbose_name="祈福語")
    description = models.TextField(blank=True, verbose_name="描述")
    is_available = models.BooleanField(default=True, verbose_name="是否可用")

    def __str__(self):
        return self.name