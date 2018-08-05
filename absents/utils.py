from datetime import date


def get_closest_school_year(d=date.today()):
    if 1 <= d.month <= 7:
        return d.year - 1
    elif 9 <= d.month <= 12:
        return d.year
    else:
        return d.year
