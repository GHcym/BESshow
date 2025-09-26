"""
EPD 管理介面視圖
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db import models

from epd_integration.services.api_client import EPDAPIClient
from epd_integration.exceptions import EPDAPIException

from .models import LanternWall, LanternPlayer
from .forms import LanternWallWithPlayersForm

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
        
        # 查找該播放器所屬的燈牆資訊
        wall_info = None
        try:
            lantern_player = LanternPlayer.objects.filter(serial_number=player.serialnum).first()
            if lantern_player:
                wall_info = {
                    'wall': lantern_player.wall,
                    'position': lantern_player.position,
                    'is_enabled': lantern_player.is_enabled
                }
        except Exception as e:
            logger.warning(f'無法取得燈牆資訊: {str(e)}')
        
        context = {
            'player': player,
            'epds': epds,
            'wall_info': wall_info,
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


# ===== 燈牆管理視圖 =====

@login_required
@user_passes_test(is_superuser)
def lantern_wall_list(request):
    """燈牆列表頁面"""
    walls = LanternWall.objects.all()
    
    # 搜尋功能
    search = request.GET.get('search')
    if search:
        walls = walls.filter(
            models.Q(name__icontains=search) | 
            models.Q(description__icontains=search)
        )
    
    # 狀態篩選
    status = request.GET.get('status')
    if status == 'active':
        walls = walls.filter(is_active=True)
    elif status == 'inactive':
        walls = walls.filter(is_active=False)
    
    # 排序
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = ['created_at', '-created_at', 'name', '-name']
    if sort in valid_sorts:
        walls = walls.order_by(sort)
    else:
        walls = walls.order_by('-created_at')

    context = {
        'walls': walls,
        'page_title': '燈牆管理',
        'total_walls': walls.count(),
        'search_query': search or '',
    }
    return render(request, 'epd_management/lantern_wall_list.html', context)


@login_required
@user_passes_test(is_superuser)
def lantern_wall_create(request):
    """新增燈牆"""
    if request.method == 'POST':
        form = LanternWallWithPlayersForm(data=request.POST)
        if form.is_valid():
            try:
                wall = form.save()
                messages.success(request, f'燈牆「{wall.name}」建立成功')
                return redirect('epd_management:lantern_wall_list')
            except Exception as e:
                messages.error(request, f'建立燈牆失敗: {str(e)}')
        else:
            messages.error(request, '表單資料無效，請檢查輸入')
    else:
        form = LanternWallWithPlayersForm()

    context = {
        'form': form,
        'page_title': '新增燈牆',
        'is_create': True
    }
    return render(request, 'epd_management/lantern_wall_form.html', context)


@login_required
@user_passes_test(is_superuser)
def lantern_wall_update(request, wall_id):
    """編輯燈牆設定"""
    logger.info(f'開始處理燈牆編輯請求: wall_id={wall_id}, method={request.method}')
    wall = get_object_or_404(LanternWall, id=wall_id)
    logger.info(f'找到燈牆: {wall.name} (ID: {wall.id})')

    if request.method == 'POST':
        logger.info(f'POST請求資料: {dict(request.POST)}')
        form = LanternWallWithPlayersForm(instance=wall, data=request.POST, files=request.FILES)
        logger.info(f'表單建立完成，檢查驗證...')

        if form.is_valid():
            logger.info('表單驗證通過，開始儲存...')
            try:
                wall = form.save()
                logger.info(f'燈牆儲存成功: {wall.name}')
                messages.success(request, f'燈牆「{wall.name}」更新成功')
                return redirect('epd_management:lantern_wall_list')
            except Exception as e:
                logger.error(f'更新燈牆失敗: {str(e)}', exc_info=True)
                messages.error(request, f'更新燈牆失敗: {str(e)}')
        else:
            logger.error(f"表單驗證失敗: wall_form_errors={form.wall_form.errors}, players_errors={form.players_formset.errors}, non_form_errors={form.non_form_errors}")
            logger.error(f"詳細表單資料: {request.POST}")
            messages.error(request, '表單資料無效，請檢查輸入')
    else:
        logger.info('GET請求，建立表單...')
        form = LanternWallWithPlayersForm(instance=wall)

    context = {
        'form': form,
        'wall': wall,
        'page_title': f'編輯燈牆 - {wall.name}',
        'is_create': False
    }
    logger.info('渲染編輯頁面')
    return render(request, 'epd_management/lantern_wall_form.html', context)


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def lantern_wall_delete(request, wall_id):
    """刪除燈牆"""
    wall = get_object_or_404(LanternWall, id=wall_id)

    try:
        wall_name = wall.name
        wall.delete()
        messages.success(request, f'燈牆「{wall_name}」已刪除')
    except Exception as e:
        messages.error(request, f'刪除燈牆失敗: {str(e)}')

    return redirect('epd_management:lantern_wall_list')


@login_required
@user_passes_test(is_superuser)
def player_status_by_serial(request, serialnum):
    """根據Player ID查看播放器狀態"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        # 嘗試根據Player ID取得播放器
        players = client.list_players()
        player = None

        for p in players:
            if p.serialnum == serialnum:
                player = p
                break

        if not player:
            messages.warning(request, f'找不到Player ID為 {serialnum} 的播放器')
            return redirect('epd_management:lantern_wall_list')

        # 取得詳細資訊
        player = client.get_player(player.id)
        epds = [epd for epd in player.epds] if player.epds else []
        epds.sort(key=lambda x: x.order)

        # 查找該播放器所屬的燈牆資訊
        wall_info = None
        try:
            lantern_player = LanternPlayer.objects.filter(serial_number=serialnum).first()
            if lantern_player:
                wall_info = {
                    'wall': lantern_player.wall,
                    'position': lantern_player.position,
                    'is_enabled': lantern_player.is_enabled
                }
        except Exception as e:
            logger.warning(f'無法取得燈牆資訊: {str(e)}')

        context = {
            'player': player,
            'epds': epds,
            'wall_info': wall_info,
            'page_title': f'播放器狀態 - {serialnum}',
            'serialnum': serialnum
        }
        return render(request, 'epd_management/player_status_by_serial.html', context)

    except EPDAPIException as e:
        messages.error(request, f'無法取得播放器狀態: {str(e)}')
        return redirect('epd_management:lantern_wall_list')


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def sync_wall_upload(request):
    """上傳同步 - 將本地配置同步到外部API"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        walls = LanternWall.objects.filter(is_active=True)

        synced_count = 0
        for wall in walls:
            for player in wall.players.filter(is_enabled=True, serial_number__isnull=False).exclude(serial_number=''):
                try:
                    # 檢查外部API是否有此播放器
                    players = client.list_players()
                    existing_player = None
                    for p in players:
                        if p.serialnum == player.serial_number:
                            existing_player = p
                            break

                    if not existing_player:
                        # 建立新播放器
                        new_player = client.create_player(player.serial_number)
                        logger.info(f'建立新播放器: {new_player.serialnum}')
                        synced_count += 1
                    else:
                        logger.info(f'播放器已存在: {existing_player.serialnum}')

                except EPDAPIException as e:
                    logger.error(f'同步播放器 {player.serial_number} 失敗: {str(e)}')

        messages.success(request, f'上傳同步完成，共處理 {synced_count} 個新播放器')
        return JsonResponse({'status': 'success', 'synced_count': synced_count})

    except Exception as e:
        logger.error(f'上傳同步失敗: {str(e)}')
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["POST"])
def sync_wall_download(request):
    """下載同步 - 從外部API同步最新狀態"""
    try:
        client = EPDAPIClient(token=settings.EPD_API_TOKEN)
        players = client.list_players()

        updated_count = 0
        for api_player in players:
            # 檢查本地是否有對應的播放器設定
            local_players = LanternPlayer.objects.filter(serial_number=api_player.serialnum)
            if local_players.exists():
                # 更新本地記錄的狀態（如果需要）
                # 這裡可以添加更多同步邏輯
                updated_count += 1

        messages.success(request, f'下載同步完成，共處理 {len(players)} 個播放器')
        return JsonResponse({'status': 'success', 'player_count': len(players)})

    except EPDAPIException as e:
        logger.error(f'下載同步失敗: {str(e)}')
        return JsonResponse({'status': 'error', 'message': str(e)})