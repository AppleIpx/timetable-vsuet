from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for timetable_vsuet.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, default="Alex")
    last_name = models.CharField(max_length=100, default="Smith")
    patronymic = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        verbose_name = "преподаватель"
        verbose_name_plural = "преподаватели"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
