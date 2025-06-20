from django.conf import settings
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from timetable.search.view import TeacherSearchView
from timetable.search.view import rebuild_opensearch_view

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

urlpatterns = [
    path("teachers/", TeacherSearchView.as_view(), name="teacher-search"),
    path(
        "rebuild-opensearch/",
        admin.site.admin_view(rebuild_opensearch_view),
        name="rebuild-opensearch",
    ),
]
