from django.urls import path
from .views import *

urlpatterns = [
    path('basket/', view_basket, name='view_basket'),
    path('success/', order_success_view, name='order_success'),
    path('basket/add/<int:product_id>/', add_to_basket, name='add_to_basket'),
    path('basket/order/', create_orders_from_basket, name='create_orders_from_basket'), 
    path('basket/delete/<int:product_id>/', delete_from_basket, name='delete_from_basket'),
    path('place/<int:product_id>/', place_order_view, name='place_order'),
]
