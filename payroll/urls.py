from django.urls import path

from payroll import views

app_name = "payroll"

urlpatterns = [
    path("sheets/", views.sheet_list, name="sheet_list"),
    path("sheets/<int:pk>/", views.sheet_detail, name="sheet_detail"),
    path("sheets/<int:pk>/pdf/", views.sheet_pdf, name="sheet_pdf"),
    path("my-payslips/", views.my_payslips, name="my_payslips"),
]
