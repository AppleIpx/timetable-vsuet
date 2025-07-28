from django_opensearch_dsl import Document
from django_opensearch_dsl import fields
from django_opensearch_dsl.registries import registry

from timetable.core.models import Subject


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
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "edge_ngram_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 20,
                    },
                },
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "edge_ngram_filter"],
                    },
                    "ngram_search_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase"],
                    },
                },
            },
        }

    class Django:
        model = Subject
        fields = (
            "id",
            "name",
        )
