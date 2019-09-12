from django.urls import path
from check_in_manager import views

urlpatterns = [
    path('', views.index, name="orders_table"),
    path('orders_table/order/<int:order_id>/details/',
         views.order_details, name='order_details'),
    path('orders_table/order/<int:order_id>/details/edit',
         views.edit_order, name='edit_order'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders_table/order/<int:order_id>/create_offers',
         views.create_offers, name='create_offers'),
    path('orders_table/order/<int:order_id>/send_offers/',
         views.send_offers, name='send_offers'),
    path('orders_table/order/<int:order_id>/accept_offer/',
         views.accept_offer, name='accept_offer'),
    path('orders_table/order/<int:order_id>/decline_offer/',
         views.decline_offer, name='decline_offer')
]
