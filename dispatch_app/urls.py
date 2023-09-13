from django.urls import path
from .views import *

app_name = 'dispatch_app'

urlpatterns = [
    path('', PlaceOrderView.as_view(), name='place_order'),
    path('order_placed/<int:order_id>/', OrderPlacedView.as_view(), name='order_placed'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order_status/<int:order_id>/', OrderStatusView.as_view(), name='order_status'),
]
