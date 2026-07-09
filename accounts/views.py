from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def home(request):
    user = request.user
    if user.is_principal:
        return redirect("staff:teacher_list")
    if user.is_discipline_master:
        return redirect("attendance:scan")
    if user.is_accountant or user.is_proprietor:
        return redirect("dashboard")
    if user.is_teacher:
        return redirect("staff:my_qr")
    return redirect("login")


@login_required
def dashboard(request):
    return render(request, "dashboard/index.html")
