from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListAPIView

from timetable.core.models import Subject
from timetable.core.serializers.list_subject_serializer import SubjectSerializer
from timetable.search.api.serializers.request_serializer import RequestSearchSerializer
from timetable.search.api.utils.django_filter import django_filter_warning
from timetable.search.query_generators.subject_search_query_generator import SubjectSearchQueryGenerator


@extend_schema_view(get=extend_schema(parameters=[RequestSearchSerializer]))
class SubjectSearchView(ListAPIView):
    request_serializer_class = RequestSearchSerializer
    serializer_class = SubjectSerializer

    @django_filter_warning  # type: ignore[arg-type]
    def get_queryset(self):
        serializer = self.request_serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        query_generator_service = SubjectSearchQueryGenerator()
        search_result = query_generator_service(**serializer.validated_data).execute()

        subject_ids = [hit.meta.id for hit in search_result]
        return Subject.objects.filter(id__in=subject_ids)
