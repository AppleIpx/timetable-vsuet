from opensearchpy import Q

from timetable.search.documents.subject_doc import SubjectDocument


class SubjectSearchQueryGenerator:
    def __call__(self, query: str):
        query = query.lower()
        q = Q(
            "bool",
            should=[
                # Поиск по названию предмета с нечетким соответствием (fuzziness="AUTO" позволяет опечатки)
                Q("match", subject_name={"query": query, "fuzziness": "AUTO"}),
                # Точное совпадение
                Q("term", **{"group_name.raw": query}),
                Q("term", **{"audience_name.raw": query}),
                # Нечеткий поиск
                Q("match", teacher_first_name={"query": query, "fuzziness": "AUTO"}),
                Q("match", teacher_last_name={"query": query, "fuzziness": "AUTO"}),
                Q("match", teacher_patronymic={"query": query, "fuzziness": "AUTO"}),
                # Поиск по частичному совпадению
                Q("wildcard", teacher_first_name=f"*{query}*"),
                Q("wildcard", teacher_last_name=f"*{query}*"),
                Q("wildcard", teacher_patronymic=f"*{query}*"),
            ],
            minimum_should_match=1,
        )

        return (
            SubjectDocument.search()
            .query(q)
            .highlight(
                "subject_name",
                "teacher_first_name",
                "teacher_last_name",
                "teacher_patronymic",
                "group_name",
                "audience_name",
            )
        )
