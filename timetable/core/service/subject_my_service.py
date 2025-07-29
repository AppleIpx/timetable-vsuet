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
        if hasattr(self.user, "student"):
            return self._get_student_subjects()
        if hasattr(self.user, "teacher"):
            return self._get_teacher_subjects()
        return Subject.objects.none()

    def _get_student_subjects(self):
        """Возвращает предметы, которые принадлежат студенту"""
        student = self.user.student
        group = student.group
        subgroup = student.subgroup

        # Предметы, которые:
        # - принадлежат нужной группе и подгруппе
        # - и либо начинаются в нужный диапазон
        # - либо имеют повторения в этом диапазоне
        return self.base_query.filter(group=group, subgroup=subgroup).filter(self._get_date_filter()).distinct()

    def _get_teacher_subjects(self):
        """Предметы, которые ведет преподаватель"""
        teacher = self.user.teacher

        # Предметы, которые ведет преподаватель отправивший запрос в периоде двух недель
        return self.base_query.filter(teacher=teacher).filter(self._get_date_filter()).distinct()

    def _get_date_filter(self):
        """
        Возвращает фильтр по датам: включает предметы, которые проходят на этой неделе
        или имеют повторения в пределах текущих двух недель.
        """
        return Q(date__range=(self.start_weekday, self.end_weekday)) | Q(
            repeat_dates__date__date__range=(self.start_weekday, self.end_weekday),
        )
