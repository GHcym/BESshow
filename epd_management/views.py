"""
EPD 管理介面視圖
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

from epd_integration.services.api_client import EPDAPIClient
from epd_integration.exceptions import EPDAPIException

logger = logging.getLogger(__name__)


def is_superuser(user):
    """檢查是否為超級管理員"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_superuser)
def player_list(request):
    """播放器列表頁面"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        players = client.list_players()
        
        context = {
            'players': players,
            'page_title': 'Player (EPD) Management'
        }
        return render(request, 'epd_management/player_list.html', context)
        
    except EPDAPIException as e:
        messages.error(request, f'無法取得播放器列表: {str(e)}')
        return render(request, 'epd_management/player_list.html', {'players': []})


@login_required
@user_passes_test(is_superuser)
def player_detail(request, player_id):
    """播放器詳細頁面"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        player = client.get_player(player_id)
        epds = [epd for epd in player.epds] if player.epds else []
        
        # 依照順序排序 EPD 設備
        epds.sort(key=lambda x: x.order)
        
        context = {
            'player': player,
            'epds': epds,
            'page_title': f'播放器 {player.serialnum}'
        }
        return render(request, 'epd_management/player_detail.html', context)
        
    except EPDAPIException as e:
        messages.error(request, f'無法取得播放器資訊: {str(e)}')
        return redirect('epd_management:player_list')


@login_required
@user_passes_test(is_superuser)
def epd_detail(request, epd_id):
    """EPD 設備詳細頁面"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        epd = client.get_epd(epd_id)
        
        context = {
            'epd': epd,
            'images': epd.images if epd.images else [],
            'page_title': f'EPD 設備 #{epd.id}'
        }
        return render(request, 'epd_management/epd_detail.html', context)
        
    except EPDAPIException as e:
        messages.error(request, f'無法取得 EPD 設備資訊: {str(e)}')
        return redirect('epd_management:player_list')


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def upload_image(request, epd_id):
    """上傳圖片到 EPD"""
    if 'image_file' not in request.FILES:
        messages.error(request, '請選擇要上傳的圖片')
        return redirect('epd_management:epd_detail', epd_id=epd_id)
    
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        image_file = request.FILES['image_file']
        
        # 上傳圖片
        image = client.upload_image(epd_id, image_file)
        messages.success(request, f'圖片上傳成功 (ID: {image.id})')
        
        # 標記 EPD 需要更新
        client.update_epd(epd_id, updated=True)
        
    except EPDAPIException as e:
        messages.error(request, f'圖片上傳失敗: {str(e)}')
    
    return redirect('epd_management:epd_detail', epd_id=epd_id)


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def delete_image(request, image_id):
    """刪除圖片"""
    epd_id = request.POST.get('epd_id')
    
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        client.delete_image(image_id)
        messages.success(request, '圖片刪除成功')
        
        # 標記 EPD 需要更新
        if epd_id:
            client.update_epd(epd_id, updated=True)
            
    except EPDAPIException as e:
        messages.error(request, f'圖片刪除失敗: {str(e)}')
    
    if epd_id:
        return redirect('epd_management:epd_detail', epd_id=epd_id)
    else:
        return redirect('epd_management:player_list')


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def sync_epd(request, epd_id):
    """同步 EPD 設備"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        client.update_epd(epd_id, updated=True)
        messages.success(request, 'EPD 設備已標記為需要同步')
        
    except EPDAPIException as e:
        messages.error(request, f'同步失敗: {str(e)}')
    
    return redirect('epd_management:epd_detail', epd_id=epd_id)


@login_required
@user_passes_test(is_superuser)
def api_status(request):
    """API 狀態檢查 (AJAX)"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        players = client.list_players()
        
        return JsonResponse({
            'status': 'success',
            'player_count': len(players),
            'message': 'API 連線正常'
        })
        
    except EPDAPIException as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })