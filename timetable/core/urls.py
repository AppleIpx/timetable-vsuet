from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern
from django.urls import URLResolver
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from timetable.core.views.audience import AudienceViewSet
from timetable.core.views.list_timetable import TimetableViewSet
from timetable.core.views.update_timetable_data import update_timetable_view

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("", TimetableViewSet)
router.register("audience", AudienceViewSet)


urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),
    path(
        "update-timetable/",
        admin.site.admin_view(update_timetable_view),
        name="update-timetable",
    ),
]
