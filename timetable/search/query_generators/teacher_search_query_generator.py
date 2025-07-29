from opensearchpy import Q

from timetable.search.documents.teacher_doc import TeacherDocument


class TeacherSearchQueryGenerator:
    def __call__(self, query: str):
        query = query.lower()
        q = Q(
            "bool",
            should=[
                # Умный поиск с опечатками
                Q("match", first_name={"query": query, "fuzziness": "AUTO"}),
                Q("match", last_name={"query": query, "fuzziness": "AUTO"}),
                Q("match", patronymic={"query": query, "fuzziness": "AUTO"}),
                # Поиск по подстроке
                Q("wildcard", first_name=f"*{query}*"),
                Q("wildcard", last_name=f"*{query}*"),
                Q("wildcard", patronymic=f"*{query}*"),
            ],
            minimum_should_match=1,
        )

        return TeacherDocument.search().query(q).highlight("first_name", "last_name", "patronymic")
