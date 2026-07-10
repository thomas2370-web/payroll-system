from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. Every login belongs to exactly one role.
    RBAC is enforced at the view/permission layer using this field,
    not by giving users individually assigned permissions.
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
        PRINCIPAL = "PRINCIPAL", "Principal"
        DISCIPLINE_MASTER = "DISCIPLINE_MASTER", "Discipline Master"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        PROPRIETOR = "PROPRIETOR", "Proprietor"
        TEACHER = "TEACHER", "Teacher"

    role = models.CharField(max_length=20, choices=Role.choices)

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN

    @property
    def is_principal(self):
        return self.role == self.Role.PRINCIPAL

    @property
    def is_discipline_master(self):
        return self.role == self.Role.DISCIPLINE_MASTER

    @property
    def is_accountant(self):
        return self.role == self.Role.ACCOUNTANT

    @property
    def is_proprietor(self):
        return self.role == self.Role.PROPRIETOR

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
