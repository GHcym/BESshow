from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        messages.warning(request, '數量必須大於0')
        return redirect('cart:cart_detail')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'已將 {product.name} 加入購物車')
    return redirect('products:product_offering_list')

def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
@require_POST
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        cart_item.delete()
        messages.success(request, f'已從購物車移除 {cart_item.product.name}')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'已更新 {cart_item.product.name} 的數量為 {quantity}')

    return redirect('cart:cart_detail')

@login_required
def remove_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'已從購物車移除 {product_name}')
    return redirect('cart:cart_detail')

@login_required
def checkout(request):
    # Build the URL for the user profile update page with a 'next' parameter
    profile_update_url = reverse('user_profile_update')
    return redirect(f'{profile_update_url}?next=payment')
