from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction
import logging

from cart.models import Cart
from .models import Order, OrderItem

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
