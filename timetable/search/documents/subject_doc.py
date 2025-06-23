from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

from timetable.core.models import Subject


@registry.register_document
class SubjectDocument(Document):
    class Index:
        name = "subjects"

    class Django:
        model = Subject
        fields = (
            "id",
            "name",
        )
