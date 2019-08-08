from django.urls import path
from .views import *

urlpatterns = [
    path('', stm_index, name="stm_index"),
    path('villa_list/', villa_list, name='villa_list'),
    path('villa_details/<id>/', villa_details, name='villa_details'),
    path('create_item/', create_item, name='create_item'),
    path('ajax_search', ajax_search, name='ajax_search'),
    # path("<int:pk>/expenses", villa_expenses, name='villa_expenses'),
]
