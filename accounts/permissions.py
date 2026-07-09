"""
Role-based access control (RBAC) permissions.

Rather than Django's default per-user permission assignment, access is
gated purely on `request.user.role`. This mirrors Table 4 in the project
report (RBAC Permissions Matrix) and enforces separation of duties:
e.g. the Discipline Master can never touch salary data, and the
Accountant can never approve a payment sheet.
"""
from __future__ import annotations

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(UserPassesTestMixin):
    """
    Class-based view mixin. Subclass and set `allowed_roles`, e.g.:

        class ScanQRView(RoleRequiredMixin, View):
            allowed_roles = ["DISCIPLINE_MASTER"]
    """
    allowed_roles: list[str] = []

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in self.allowed_roles

    def handle_no_permission(self):
        raise PermissionDenied("Your role does not permit this action.")


def role_required(*roles):
    """Function-based view decorator equivalent of RoleRequiredMixin."""
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role not in roles:
                raise PermissionDenied("Your role does not permit this action.")
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
