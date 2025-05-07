from django.urls import resolve
from django.urls import reverse

from timetable.users.models import User


def test_user_detail(user: User):
    assert reverse("api:users:user-detail", kwargs={"username": user.username}) == f"/api/users/{user.username}/"
    assert resolve(f"/api/users/{user.username}/").view_name == "api:users:user-detail"


def test_user_list():
    assert reverse("api:users:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:users:user-list"


def test_user_me():
    assert reverse("api:users:user-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:users:user-me"
