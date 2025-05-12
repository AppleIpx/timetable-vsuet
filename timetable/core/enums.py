# Дни недели
MONDAY = "monday"
TUESDAY = "tuesday"
WEDNESDAY = "wednesday"
THURSDAY = "thursday"
FRIDAY = "friday"
SATURDAY = "saturday"
SUNDAY = "sunday"

# Тип недели
NUMERATOR = "numerator"
DENOMINATOR = "denominator"

# Тип занятия
LECTURE = "lecture"
PRACTICE = "practice"
LABORATORY = "laboratory"

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
]

TYPE_OF_CLASSES_CHOICES = [
    (LECTURE, "Лекция"),
    (PRACTICE, "Практическое занятие"),
    (LABORATORY, "Лабораторное занятие"),
]
