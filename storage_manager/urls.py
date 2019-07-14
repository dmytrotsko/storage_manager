from django.urls import path
from .views import stm_index

urlpatterns = [
    path('', stm_index, name="stm_index"),
    # path("<int:pk>/expenses", villa_expenses, name='villa_expenses'),
]
