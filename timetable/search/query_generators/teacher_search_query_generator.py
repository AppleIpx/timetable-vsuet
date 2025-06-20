from opensearchpy import Q

from timetable.search.documents.teacher_doc import TeacherDocument


class TeacherSearchQueryGenerator:
    def __call__(self, query: str):
        q = Q(
            "bool",
            should=[
                Q("prefix", first_name=query.lower()),
                Q("prefix", last_name=query.lower()),
                Q("prefix", patronymic=query.lower()),
            ],
            minimum_should_match=1,
        )

        return TeacherDocument.search().query(q).highlight("first_name", "last_name", "patronymic")
