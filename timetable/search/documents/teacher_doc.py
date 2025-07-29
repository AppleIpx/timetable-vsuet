from django_opensearch_dsl import Document
from django_opensearch_dsl import fields
from django_opensearch_dsl.registries import registry

from timetable.search.settings import COMMON_INDEX_SETTINGS
from timetable.users.models import Teacher


@registry.register_document
class TeacherDocument(Document):
    first_name = fields.TextField(
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )
    last_name = fields.TextField(
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )
    patronymic = fields.TextField(
        analyzer="ngram_analyzer",
        search_analyzer="ngram_search_analyzer",
    )

    class Index:
        name = "teachers"
        settings = COMMON_INDEX_SETTINGS

    class Django:
        model = Teacher
        fields = ("id",)
