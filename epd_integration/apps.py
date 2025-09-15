"""
EPD Integration Django App Configuration
"""
from django.apps import AppConfig


class EpdIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'epd_integration'
    verbose_name = 'EPD Integration'