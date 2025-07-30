from timetable.core.models import Subject
from timetable.search.documents.subject_doc import SubjectDocument
from timetable.search.documents.teacher_doc import TeacherDocument


def update_teacher_opensearch_index(teacher) -> None:
    """Функция, которая обновляет данные о преподавателе в opensearch"""
    # Индексируем преподавателя
    TeacherDocument().update([teacher], action="index")

    # Принудительно обновляем индекс
    TeacherDocument._index.refresh()  # noqa: SLF001


def update_subject_opensearch_index(subject: Subject | list[Subject]) -> None:
    """Функция, которая обновляет данные о предмете в opensearch"""
    if isinstance(subject, Subject):
        # Индексируем предмет
        SubjectDocument().update([subject], action="index")
    else:
        SubjectDocument().update(subject, action="index")

    # Принудительно обновляем индекс
    SubjectDocument._index.refresh()  # noqa: SLF001
