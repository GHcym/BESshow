
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('payment/', views.payment_page, name='payment_page'),
    path('create/', views.create_order, name='create_order'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('history/', views.order_history, name='order_history'),
    path('lantern-orders/', views.lantern_order_list, name='lantern_order_list'),
    path('order-items/', views.order_item_list, name='order_item_list'),
    path('order-items/<int:order_item_id>/pair/', views.order_item_pairing, name='order_item_pairing'),
    path('order-items/<int:order_item_id>/preview/', views.preview_lantern_image, name='preview_lantern_image'),
]
