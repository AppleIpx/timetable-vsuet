from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Student
from .models import Teacher
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class BaseUserAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        """Метод для динамического управления полями"""
        all_fields = [field.name for field in self.model._meta.fields]  # noqa: SLF001
        base_fields = [f for f in all_fields if f not in ("user", "id")]
        if obj is None:
            base_fields = [f for f in base_fields if f != "password"]
        return base_fields


@admin.register(Teacher)
class TeacherAdmin(BaseUserAdmin):
    search_fields = ["last_name"]
    exclude = ["user"]


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
    search_fields = ["last_name", "group", "faculty"]
    exclude = ["user"]
