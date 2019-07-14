from django.urls import path
from .views import villa_list, villa_expenses


urlpatterns = [
    path('', villa_list, name="villas_list"),
    path("/<int:pk>/expenses", villa_expenses, name='villa_expenses'),
    path("/<int:pk>/reports", villa_reports, name='villa_reports'),
]
