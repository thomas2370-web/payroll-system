from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from staff.models import Teacher
from .models import User


def custom_login(request):
    """
    Custom login that allows role-based authentication.
    Non-teacher roles authenticate by username + password, while teacher
    accounts require an additional subject match.
    """
    if request.method == "POST":
        role = request.POST.get("role")
        password = request.POST.get("password")

        if not role:
            return render(request, "registration/login.html", {"error": "Please select a role."})

        username = request.POST.get("username") or ""
        if role == "TEACHER":
            subject = request.POST.get("subject") or ""
            if not username or not subject:
                return render(request, "registration/login.html", {"error": "Please enter your username and subject."})

            teacher = Teacher.objects.filter(user__username=username, subject__iexact=subject).first()
            if teacher is None:
                user = User.objects.create_user(username=username, password=password, role=role)
                teacher = Teacher.objects.create(user=user, name=username, subject=subject, hourly_rate=0, expected_weekly_hours=0)
            else:
                user = teacher.user
        else:
            if not username:
                return render(request, "registration/login.html", {"error": "Please enter a username."})

            user = User.objects.filter(username=username).first()
            if user is None:
                user = User.objects.create_user(username=username, password=password, role=role)
            elif user.role != role:
                return render(request, "registration/login.html", {"error": "Role does not match user account."})

        if not user.check_password(password):
            return render(request, "registration/login.html", {"error": "Invalid password."})

        login(request, user)
        next_url = request.POST.get("next", "")
        if not next_url or next_url.strip() == "":
            next_url = "home"
        return redirect(next_url)

    context = {
        "next": request.GET.get("next", ""),
    }
    return render(request, "registration/login.html", context)


@login_required
def home(request):
    user = request.user
    if user.is_super_admin:
        return redirect("dashboard")
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
