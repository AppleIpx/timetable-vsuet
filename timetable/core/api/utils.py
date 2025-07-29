from datetime import timedelta


def get_two_week_range(current_date):
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_next_week = start_of_week + timedelta(days=13)
    return start_of_week, end_of_next_week
