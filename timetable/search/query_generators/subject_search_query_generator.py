from opensearchpy import Q

from timetable.search.documents.subject_doc import SubjectDocument


class SubjectSearchQueryGenerator:
    def __call__(self, query: str):
        q = Q(
            "bool",
            should=[
                Q("prefix", name=query.lower()),
            ],
            minimum_should_match=1,
        )

        return SubjectDocument.search().query(q).highlight("name")
