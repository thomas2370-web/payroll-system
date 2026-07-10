from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.forms import StyledAuthenticationForm
from accounts.views import custom_login, dashboard, delete_user, home, reset_user_password

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/users/<int:user_id>/reset-password/", reset_user_password, name="reset_user_password"),
    path("dashboard/users/<int:user_id>/delete/", delete_user, name="delete_user"),
    path("login/", custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("staff/", include("staff.urls")),
    path("attendance/", include("attendance.urls")),
    path("payroll/", include("payroll.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
