from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from timetable.search.api.utils.rebuild_opensearch import rebuild_opensearch_view
from timetable.search.api.views.subject_view import SubjectSearchView
from timetable.search.api.views.teacher_view import TeacherSearchView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

urlpatterns = [
    path("teachers/", TeacherSearchView.as_view(), name="teacher-search"),
    path("subjects/", SubjectSearchView.as_view(), name="subject-search"),
    path(
        "rebuild-opensearch/",
        admin.site.admin_view(rebuild_opensearch_view),
        name="rebuild-opensearch",
    ),
    path("", include(router.urls)),
]
