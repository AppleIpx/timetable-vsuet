from datetime import date

from django.core.exceptions import ValidationError


def calculating_a_type_of_week(target_date: date, start_date_semester):
    """
    Функция для расчета типа недели предмета(числитель/знаменатель),
    исходя от даты начала семестра и даты начала предмета.
    """
    if start_date_semester and start_date_semester.start_date and start_date_semester.end_date:
        """
        Возвращает "numerator" или "denominator" для переданной даты.
        """
        if target_date < start_date_semester.start_date or target_date > start_date_semester.end_date:
            msg_error = (
                f"Дата вне диапазона семестра, сейчас дата начала семестра стоит на {start_date_semester.start_date}"
            )
            raise ValidationError(msg_error)

        delta_weeks = (target_date - start_date_semester.start_date).days // 7

        if start_date_semester.week_type == "numerator":
            return "numerator" if delta_weeks % 2 == 0 else "denominator"
        return "denominator" if delta_weeks % 2 == 0 else "numerator"
    msg_error = "У вас не выставлены даты начала и конца семестра"
    raise ValidationError(msg_error)
