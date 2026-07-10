from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.forms import StyledAuthenticationForm
from accounts.views import custom_login, dashboard, home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("staff/", include("staff.urls")),
    path("attendance/", include("attendance.urls")),
    path("payroll/", include("payroll.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
