from django.urls import path
from check_in_manager import views

urlpatterns = [
    path('', views.index, name="orders_table"),
    path('orders_table/order/<int:order_id>/details/', views.order_details, name='order_details'),
    path('orders_table/order/<int:order_id>/details/edit', views.edit_order, name='edit_order'),
    path('create_order/', views.create_order, name='create_order')
]
