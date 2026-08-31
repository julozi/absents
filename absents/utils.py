from datetime import date


def get_closest_school_year(d=None):
    d = d or date.today()
    if 1 <= d.month <= 7:
        return d.year - 1
    else:
        return d.year
