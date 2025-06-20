from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListAPIView

from timetable.search.query_generators.teacher_search_query_generator import TeacherSearchQueryGenerator
from timetable.search.serializer import RequestSearchSerializer
from timetable.search.serializer import TeacherSearchSerializer
from timetable.search.service import ALLOWED_INDEXES
from timetable.search.service import CommandType
from timetable.search.service import OpensearchCommandExecutor
from timetable.search.utils import django_filter_warning


@staff_member_required
def rebuild_opensearch_view(request):
    if request.method == "POST":
        command_type = CommandType.index if CommandType.index.value in request.POST else CommandType.document
        index = request.POST[command_type.value]
        command_executor = OpensearchCommandExecutor()
        message = command_executor(command_type, index)

        return render(
            request,
            "admin/opensearch/rebuild_result.html",
            {"message": message},
        )

    return render(
        request,
        "admin/opensearch/rebuild_opensearch.html",
        {"indexes": ALLOWED_INDEXES},
    )


@extend_schema_view(get=extend_schema(parameters=[RequestSearchSerializer]))
class TeacherSearchView(ListAPIView):
    request_serializer_class = RequestSearchSerializer
    serializer_class = TeacherSearchSerializer

    @django_filter_warning  # type: ignore[arg-type]
    def get_queryset(self):
        serializer = self.request_serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        query_generator_service = TeacherSearchQueryGenerator()
        return query_generator_service(**serializer.validated_data).execute()
