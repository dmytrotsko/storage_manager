from django.urls import path
from .views import index, order_details, edit_order

urlpatterns = [
    path('', index, name="orders_table"),
    path('orders_table/order/<int:order_id>/details/', order_details),
    path('orders_table/order/<int:order_id>/details/edit', edit_order, name='edit_order'),
]
