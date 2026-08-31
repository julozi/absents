from datetime import date, timedelta


def get_closest_school_year(d=None):
    d = d or date.today()
    if 1 <= d.month <= 7:
        return d.year - 1
    else:
        return d.year


def date_from_isocalendar(iso_year, iso_week, iso_day):
    """Date grégorienne correspondant à une date au calendrier ISO 8601.

    Équivalent de datetime.date.fromisocalendar() (indisponible avant Python 3.8).
    iso_day : 1 = lundi ... 7 = dimanche.
    """
    # Le 4 janvier appartient toujours à la semaine 1 ISO.
    jan4 = date(iso_year, 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    return week1_monday + timedelta(days=(iso_week - 1) * 7 + (iso_day - 1))
