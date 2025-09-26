from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
from django.conf import settings
from django.http import JsonResponse, Http404
from django.utils import timezone
import logging
import json

from cart.models import Cart
from .models import Order, OrderItem, OrderItemPlayerAssignment
from epd_management.models import LanternWall, LanternPlayer
from .services.image_generator import LanternImageGenerator
from .services.image_upload_service import ImageUploadService

logger = logging.getLogger(__name__)

@login_required
def payment_page(request):
    user = request.user
    required_fields = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'address_county': user.address_county,
        'address_district': user.address_district,
        'address_detail': user.address_detail,
        'address_zip_code': user.address_zip_code,
    }

    for field_name, field_value in required_fields.items():
        if not field_value:
            logger.warning(f"User {user.email} has an incomplete profile. Missing or empty field: '{field_name}'. Redirecting to edit profile.")
            return redirect(f"{reverse('user_profile_update')}?next=payment")

    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            logger.warning(f"User {request.user.email} accessed payment page with an empty cart.")
            return redirect('cart:cart_detail')
    except Cart.DoesNotExist:
        logger.warning(f"User {request.user.email} accessed payment page without a cart.")
        return redirect('cart:cart_detail')
        
    return render(request, 'orders/payment.html', {'cart': cart})

@login_required
@require_POST
def create_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            logger.warning(f"User {request.user.email} attempted to create an order from an empty cart.")
            return redirect('cart:cart_detail')
    except Cart.DoesNotExist:
        logger.error(f"User {request.user.email} attempted to create an order without a cart.")
        return redirect('cart:cart_detail')

    try:
        with transaction.atomic():
            logger.info(f"Starting order creation for user {request.user.email}.")
            
            order = Order.objects.create(
                user=request.user,
                full_name=f"{request.user.last_name}{request.user.first_name}",
                email=request.user.email,
                phone_number=request.user.phone_number,
                address=f"{request.user.address_zip_code}{request.user.address_county}{request.user.address_district}{request.user.address_detail}",
                total_paid=cart.total_price,
                paid=True
            )
            logger.info(f"Order {order.id} created for user {request.user.email}.")

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            logger.info(f"Order items created for order {order.id}.")
            
            cart.items.all().delete()
            cart.delete()
            logger.info(f"Cart cleared for user {request.user.email}.")

        logger.info(f"Redirecting user {request.user.email} to confirmation for order {order.id}.")
        return redirect('orders:order_confirmation', order_id=order.id)

    except Exception as e:
        logger.error(f"Error creating order for user {request.user.email}: {e}", exc_info=True)
        return redirect('cart:cart_detail')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders/history.html', {'page_obj': page_obj})

@login_required
def lantern_order_list(request):
    orders = Order.objects.filter(processing_status='pending').prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/lantern_order_list.html', {'orders': orders})

@login_required
def order_item_list(request):
    # 篩選未配對的OrderItem：order.processing_status != 'completed' 且無配對記錄
    queryset = OrderItem.objects.filter(
        order__processing_status__in=['pending', 'processing', 'failed']
    ).exclude(
        orderitemplayerassignment__isnull=False
    ).select_related('order', 'product').order_by('-order__created_at')

    # 如果不是管理員，只顯示自己的訂單項目
    if not (request.user.is_staff or request.user.is_superuser):
        queryset = queryset.filter(order__user=request.user)

    order_items = queryset

    # 計算今日已配對數量（根據用戶時區）
    today = timezone.now().date()
    today_paired_count = OrderItemPlayerAssignment.objects.filter(
        assigned_at__date=today
    ).count()

    return render(request, 'orders/order_item_list.html', {
        'order_items': order_items,
        'today_paired_count': today_paired_count
    })

@login_required
def order_item_pairing(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # 檢查權限：管理員可以配對任何項目，普通用戶只能配對自己的
    if not (request.user.is_staff or request.user.is_superuser) and order_item.order.user != request.user:
        logger.warning(f"User {request.user.email} attempted to access pairing page for OrderItem {order_item_id} belonging to another user")
        return redirect('orders:order_item_list')

    processing_status = None
    processing_message = None

    logger.info(f"Entering order_item_pairing for OrderItem {order_item_id}, method: {request.method}")

    if request.method == 'POST':
        wall_id = request.POST.get('wall_id')
        player_id = request.POST.get('player_id')
        epd_id = request.POST.get('epd_id')

        logger.info(f"POST request for OrderItem {order_item.id} pairing: wall_id={wall_id}, player_id={player_id}, epd_id={epd_id}, user={request.user.email}")

        if wall_id and player_id and epd_id:
            try:
                wall = LanternWall.objects.get(id=wall_id)
                player = LanternPlayer.objects.get(id=player_id, wall=wall)

                # 驗證EPD屬於該Player
                from epd_integration.services.api_client import EPDAPIClient
                client = EPDAPIClient(token=settings.EPD_API_TOKEN)
                players = client.list_players(serialnum=player.serial_number)
                if not players:
                    raise ValueError(f"Player {player.serial_number} not found in EPD API")

                epd_player = players[0]
                target_epd = None
                for epd in epd_player.epds:
                    if epd.id == int(epd_id):
                        target_epd = epd
                        break

                if not target_epd:
                    raise ValueError(f"EPD {epd_id} not found for Player {player.serial_number}")

                # 檢查是否已有配對記錄
                existing_assignment = OrderItemPlayerAssignment.objects.filter(
                    order_item=order_item,
                    epd_id=epd_id
                ).first()

                if existing_assignment:
                    logger.warning(f"Duplicate pairing attempt for OrderItem {order_item.id} with EPD {epd_id} (existing assignment id: {existing_assignment.id})")
                else:
                    logger.info(f"No existing assignment found for OrderItem {order_item.id} with EPD {epd_id}")

                # 創建配對記錄
                assignment = OrderItemPlayerAssignment.objects.create(
                    order_item=order_item,
                    player=player,
                    epd_id=epd_id,
                    assigned_by=request.user
                )

                logger.info(f"OrderItem {order_item.id} paired with EPD {epd_id} (Player: {player.serial_number}) by {request.user.email}")

                # 配對成功後，自動處理圖片生成和上傳
                try:
                    processing_status = 'processing'
                    processing_message = '正在生成圖片...'

                    # 生成圖片
                    image_generator = LanternImageGenerator()
                    image_filename = image_generator.generate_image(order_item)
                    logger.info(f"圖片生成成功: {image_filename} for OrderItem {order_item.id}")

                    processing_message = '圖片生成完成，正在上傳到設備...'

                    # 上傳圖片到EPD
                    upload_service = ImageUploadService()
                    upload_success = upload_service.upload_image(assignment)

                    if upload_success:
                        logger.info(f"圖片上傳成功 for OrderItem {order_item.id}")
                        processing_status = 'completed'
                        processing_message = '配對和圖片處理全部完成！'
                    else:
                        logger.warning(f"圖片上傳失敗 for OrderItem {order_item.id}")
                        processing_status = 'completed_with_warning'
                        processing_message = '配對成功，但圖片上傳失敗。請稍後重試上傳。'

                except Exception as e:
                    logger.error(f"圖片處理失敗 for OrderItem {order_item.id}: {str(e)}")
                    processing_status = 'completed_with_error'
                    processing_message = f'配對成功，但圖片處理失敗：{str(e)}'

            except (LanternWall.DoesNotExist, LanternPlayer.DoesNotExist):
                logger.error(f"Invalid wall or player selection for OrderItem {order_item.id}")
                processing_status = 'error'
                processing_message = '無效的燈牆或播放器選擇'

    # GET 請求或處理完成後顯示頁面
    walls = LanternWall.objects.filter(is_active=True).prefetch_related('players')

    # 獲取所有EPD數據用於前端
    from epd_integration.services.api_client import EPDAPIClient
    client = EPDAPIClient(token=settings.EPD_API_TOKEN)

    walls_with_epds = []
    for wall in walls:
        wall_data = {
            'id': wall.id,
            'name': wall.name,
            'players': []
        }
        for player in wall.players.filter(is_enabled=True):
            try:
                players = client.list_players(serialnum=player.serial_number)
                if players:
                    epd_player = players[0]
                    player_data = {
                        'id': player.id,
                        'position': player.position,
                        'serial': player.serial_number,
                        'epds': [
                            {'id': epd.id, 'order': epd.order}
                            for epd in epd_player.epds
                        ]
                    }
                    wall_data['players'].append(player_data)
            except Exception as e:
                logger.warning(f"Failed to get EPDs for player {player.serial_number}: {e}")
                # 如果API失敗，至少提供player資訊
                player_data = {
                    'id': player.id,
                    'position': player.position,
                    'serial': player.serial_number,
                    'epds': []
                }
                wall_data['players'].append(player_data)

        walls_with_epds.append(wall_data)

    return render(request, 'orders/order_item_pairing.html', {
        'order_item': order_item,
        'walls': walls_with_epds,
        'processing_status': processing_status,
        'processing_message': processing_message
    })

@login_required
def preview_lantern_image(request, order_item_id):
    """
    生成燈籠圖片的預覽

    Args:
        request: HTTP請求
        order_item_id: 訂單項目ID

    Returns:
        JSON回應包含base64編碼的圖片資料
    """
    # 檢查權限：確保用戶只能預覽自己的訂單項目，或管理員可以預覽任何項目
    order_item = get_object_or_404(OrderItem, id=order_item_id)

    # 檢查用戶權限：Staff 就有權限，可以預覽任何項目
    if not (request.user.is_staff or request.user.is_superuser):
        logger.warning(f"User {request.user.email} attempted to access OrderItem {order_item_id} without staff permission")
        return JsonResponse({'error': '無權限訪問此訂單項目'}, status=403)

    try:
        # 生成預覽圖片
        image_generator = LanternImageGenerator()
        image_data = image_generator.generate_preview_image(order_item)

        logger.info(f"成功生成預覽圖片 for OrderItem {order_item_id} by user {request.user.email}")

        return JsonResponse({
            'image_data': image_data
        })

    except Exception as e:
        logger.error(f"預覽圖片生成失敗 for OrderItem {order_item_id}: {str(e)}")
        return JsonResponse({'error': f'預覽圖片生成失敗: {str(e)}'}, status=500)
