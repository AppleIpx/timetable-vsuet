from django.db.models import Q

from timetable.core.api.utils import get_two_week_range
from timetable.core.models import Subject


class MySubjectService:
    def __init__(self, base_query, current_time, user):
        self.base_query = base_query
        self.current_time = current_time
        self.start_weekday, self.end_weekday = get_two_week_range(current_date=current_time)
        self.user = user

    def __call__(self):
        return self._get_subjects()

    def _get_subjects(self):
        student = getattr(self.user, "student", None)
        if not student:
            return Subject.objects.none()

        group = student.group
        subgroup = student.subgroup

        # Предметы, которые:
        # - принадлежат нужной группе и подгруппе
        # - и либо начинаются в нужный диапазон
        # - либо имеют повторения в этом диапазоне
        return (
            self.base_query.filter(
                group=group,
                subgroup=subgroup,
            )
            .filter(
                Q(date__range=(self.start_weekday, self.end_weekday))
                | Q(repeat_dates__date__date__range=(self.start_weekday, self.end_weekday)),
            )
            .distinct()
        )
