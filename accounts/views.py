from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from staff.models import Teacher
from .models import User


def custom_login(request):
    """
    Custom login that allows role selection and teacher selection.
    For teachers, they select their name from a list instead of typing a username.
    """
    if request.method == "POST":
        role = request.POST.get("role")
        password = request.POST.get("password")
        
        if role == "TEACHER":
            teacher_id = request.POST.get("teacher_id")
            if not teacher_id:
                return render(request, "registration/login.html", {"error": "Please select a teacher."})
            try:
                teacher = Teacher.objects.get(id=teacher_id)
                user = teacher.user
            except Teacher.DoesNotExist:
                return render(request, "registration/login.html", {"error": "Teacher not found."})
        else:
            username = request.POST.get("username")
            if not username:
                return render(request, "registration/login.html", {"error": "Please enter a username."})
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return render(request, "registration/login.html", {"error": "User not found."})
        
        # Verify password and role match
        if user.check_password(password):
            if user.role == role:
                login(request, user)
                next_url = request.POST.get("next", "")
                if not next_url or next_url.strip() == "":
                    next_url = "home"
                return redirect(next_url)
            else:
                return render(request, "registration/login.html", {"error": "Role does not match user account.", "teachers": Teacher.objects.filter(is_active=True).select_related("user").order_by("name")})
        else:
            return render(request, "registration/login.html", {"error": "Invalid password."})
    
    # GET request - show login form
    teachers = Teacher.objects.filter(is_active=True).select_related("user").order_by("name")
    context = {
        "teachers": teachers,
        "next": request.GET.get("next", ""),
    }
    return render(request, "registration/login.html", context)


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
