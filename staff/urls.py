from django.urls import path

from staff import views

app_name = "staff"

urlpatterns = [
    path("teachers/register/", views.teacher_register, name="teacher_register"),
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("teachers/<int:pk>/qr/", views.teacher_qr, name="teacher_qr"),
    path("fixed-staff/", views.fixedstaff_list, name="fixedstaff_list"),
    path("my-qr/", views.my_qr, name="my_qr"),
]
