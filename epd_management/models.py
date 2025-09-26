"""
燈牆管理資料模型
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class LanternWall(models.Model):
    """燈牆模型 - 每面燈牆由12個EPD Player組成"""
    name = models.CharField(max_length=100, verbose_name="燈牆名稱")
    description = models.TextField(blank=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="啟用狀態")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "燈牆"
        verbose_name_plural = "燈牆管理"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def active_players_count(self):
        """啟用的播放器數量"""
        return self.players.filter(is_enabled=True).count()

    @property
    def configured_players_count(self):
        """已配置Player ID的播放器數量"""
        return self.players.exclude(serial_number='').count()


class LanternPlayer(models.Model):
    """燈牆播放器模型 - 燈牆中的每個播放器位置"""
    wall = models.ForeignKey(
        LanternWall,
        on_delete=models.CASCADE,
        related_name='players',
        verbose_name="所屬燈牆"
    )
    position = models.PositiveIntegerField(verbose_name="位置 (1-12)")
    serial_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Player ID"
    )
    is_enabled = models.BooleanField(default=True, verbose_name="啟用狀態")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    class Meta:
        verbose_name = "燈牆播放器"
        verbose_name_plural = "燈牆播放器"
        unique_together = ['wall', 'position']
        ordering = ['position']

    def __str__(self):
        return f"{self.wall.name} - 位置 {self.position}"

    @property
    def is_configured(self):
        """是否已配置Player ID"""
        return bool(self.serial_number.strip())