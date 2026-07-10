from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from accounts.permissions import role_required
from staff.forms import FixedStaffForm, TeacherForm
from staff.models import FixedStaff, Teacher


@login_required
@role_required("PRINCIPAL")
def teacher_register(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            teacher_user = User.objects.filter(username=username).first()

            if teacher_user is None:
                teacher_user = User.objects.create_user(
                    username=username,
                    password=password,
                    role=User.Role.TEACHER,
                    first_name="",
                    last_name="",
                )
            else:
                if teacher_user.role != User.Role.TEACHER:
                    messages.error(request, "That username is already assigned to another role.")
                    return render(request, "staff/teacher_register.html", {"form": form})
                teacher_user.role = User.Role.TEACHER
                teacher_user.set_password(password)
                teacher_user.save(update_fields=["role", "password"])

            teacher = form.save(commit=False)
            teacher.user = teacher_user
            teacher.save()
            messages.success(request, f"{teacher.name} registered and QR code generated.")
            return redirect("staff:teacher_list")
    else:
        form = TeacherForm()
    return render(request, "staff/teacher_register.html", {"form": form})


@login_required
@role_required("PRINCIPAL", "DISCIPLINE_MASTER", "ACCOUNTANT")
def teacher_list(request):
    teachers = Teacher.objects.filter(is_active=True).order_by("name")
    return render(request, "staff/teacher_list.html", {"teachers": teachers})


@login_required
@role_required("PRINCIPAL", "DISCIPLINE_MASTER")
def teacher_qr(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, "staff/teacher_qr.html", {"teacher": teacher})


@login_required
@role_required("ACCOUNTANT")
def fixedstaff_list(request):
    if request.method == "POST":
        form = FixedStaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fixed-salary staff member added.")
            return redirect("staff:fixedstaff_list")
    else:
        form = FixedStaffForm()
    staff_members = FixedStaff.objects.filter(is_active=True).order_by("name")
    return render(request, "staff/fixedstaff_list.html", {"form": form, "staff_members": staff_members})


@login_required
@role_required("TEACHER")
def my_qr(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, "staff/teacher_qr.html", {"teacher": teacher})
