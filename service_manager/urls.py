from django.urls import path
from .views import villa_list, villa_expenses, villa_reports, generate_update_report


urlpatterns = [
    path('', villa_list, name="villas_list"),
    path("<int:pk>/expenses", villa_expenses, name='villa_expenses'),
    path("<int:villa_id>/reports", villa_reports, name='villa_reports'),
    path("<int:villa_id>/reports/new_report", generate_update_report, name='new_report'),
    path("<int:villa_id>/reports/<int:report_id>", generate_update_report, name='edit_report'),

]
