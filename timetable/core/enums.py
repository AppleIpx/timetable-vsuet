# Дни недели
MONDAY = "Понедельник"
TUESDAY = "Вторник"
WEDNESDAY = "Среда"
THURSDAY = "Четверг"
FRIDAY = "Пятница"
SATURDAY = "Суббота"
SUNDAY = "Воскресенье"

# Тип недели
NUMERATOR = "Числитель"
DENOMINATOR = "Знаменатель"
AUTO = "Автоматически"

# Тип занятия
LECTURE = "Лекция"
PRACTICE = "Практическое занятие"
LABORATORY = "Лабораторное занятие"

# Тип повторения
WITHOUT_REPETITION = "Без повторения"
EveryWeek = "Каждую неделю"
EveryTwoWeeks = "Каждые 2 недели"

TYPE_OF_DAY_CHOICES = [
    (MONDAY, "Понедельник"),
    (TUESDAY, "Вторник"),
    (WEDNESDAY, "Среда"),
    (THURSDAY, "Четверг"),
    (FRIDAY, "Пятница"),
    (SATURDAY, "Суббота"),
]

TYPE_OF_WEEK_CHOICES = [
    (NUMERATOR, "Числитель"),
    (DENOMINATOR, "Знаменатель"),
    (AUTO, "Автоматически"),
]

TYPE_OF_CLASSES_CHOICES = [
    (LECTURE, "Лекция"),
    (PRACTICE, "Практическое занятие"),
    (LABORATORY, "Лабораторное занятие"),
]

RULE_OF_REPEATS = [
    (WITHOUT_REPETITION, "Без повторения"),
    (EveryWeek, "Каждую неделю"),
    (EveryTwoWeeks, "Каждые 2 недели"),
]
