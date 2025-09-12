
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('payment/', views.payment_page, name='payment_page'),
    path('create/', views.create_order, name='create_order'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('history/', views.order_history, name='order_history'),
]
