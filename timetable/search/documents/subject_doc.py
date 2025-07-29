from django_opensearch_dsl import Document
from django_opensearch_dsl import fields
from django_opensearch_dsl.registries import registry

from timetable.core.models import Subject
from timetable.search.settings import COMMON_INDEX_SETTINGS


@registry.register_document
class SubjectDocument(Document):
    teacher_first_name = fields.TextField(
        attr="teacher.first_name",
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )
    teacher_last_name = fields.TextField(
        attr="teacher.last_name",
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )
    teacher_patronymic = fields.TextField(
        attr="teacher.patronymic",
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )
    group_name = fields.TextField(attr="group.name", fields={"raw": fields.KeywordField()})
    audience_name = fields.TextField(attr="audience.name")
    subject_name = fields.TextField(
        attr="name",
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )

    class Index:
        name = "subjects"
        settings = COMMON_INDEX_SETTINGS

    class Django:
        model = Subject
        fields = (
            "id",
            "name",
        )
