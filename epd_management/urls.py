"""
EPD 管理介面 URL 配置
"""
from django.urls import path
from . import views

app_name = 'epd_management'

urlpatterns = [
    # 播放器管理
    path('', views.player_list, name='player_list'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    
    # EPD 設備管理
    path('epd/<int:epd_id>/', views.epd_detail, name='epd_detail'),
    path('epd/<int:epd_id>/sync/', views.sync_epd, name='sync_epd'),
    
    # 圖片管理
    path('epd/<int:epd_id>/upload/', views.upload_image, name='upload_image'),
    path('image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    
    # API 狀態
    path('api/status/', views.api_status, name='api_status'),
    # 燈牆管理
    path('wall/', views.lantern_wall_list, name='lantern_wall_list'),
    path('wall/create/', views.lantern_wall_create, name='lantern_wall_create'),
    path('wall/<int:wall_id>/edit/', views.lantern_wall_update, name='lantern_wall_update'),
    path('wall/<int:wall_id>/delete/', views.lantern_wall_delete, name='lantern_wall_delete'),

    # 根據Player ID查看播放器狀態
    path('player/<str:serialnum>/', views.player_status_by_serial, name='player_status_by_serial'),

    # 同步功能
    path('wall/sync/upload/', views.sync_wall_upload, name='sync_wall_upload'),
    path('wall/sync/download/', views.sync_wall_download, name='sync_wall_download'),
]