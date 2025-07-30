from django.conf import settings
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from timetable.users.api.views.teachers import TeacherView
from timetable.users.api.views.user import UserInfoView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("teachers", TeacherView, basename="teachers")

app_name = "users"

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),
    path("me/", UserInfoView.as_view(), name="user-info"),
]
