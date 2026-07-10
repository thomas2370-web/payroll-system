from django.urls import path

from attendance import views

app_name = "attendance"

urlpatterns = [
    path("scan/", views.scan, name="scan"),
    path("log/", views.log, name="log"),
    path("log/<int:record_id>/penalty/", views.add_adjustment, name="add_adjustment"),
    path("teachers/<int:teacher_id>/adjustments/", views.teacher_adjustment_history, name="teacher_adjustment_history"),
]
