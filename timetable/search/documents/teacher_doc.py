from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

from timetable.users.models import Teacher


@registry.register_document
class TeacherDocument(Document):
    class Index:
        name = "teachers"

    class Django:
        model = Teacher
        fields = (
            "id",
            "first_name",
            "last_name",
            "patronymic",
        )
