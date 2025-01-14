from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, request
from absents.domain import Absence

bp_reports = Blueprint('reports', __name__)


@bp_reports.route('/absences')
def absences():
    if 'week' not in request.args or 'year' not in request.args:
        today = date.today()
        print(today)
        week = today.isocalendar()[1]
        print(week)
        year = today.year
    else:
        week = int(request.args['week'])
        year = int(request.args['year'])

    first_day = datetime.strptime('%s-%s-1' % (year,  week - 1 if year == 2025 else week), "%Y-%W-%w")
    last_day = first_day + timedelta(days=6)

    print(first_day)

    month = first_day.month

    absences = Absence.query\
                      .filter(Absence.date >= first_day)\
                      .filter(Absence.date <= last_day)\
                      .filter(Absence.reason == None)\
                      .order_by(Absence.student_id, Absence.date)\
                      .all()  # noqa

    students = {}
    for absence in absences:
        if absence.student not in students:
            students[absence.student] = []
        students[absence.student].append(absence)

    previous_monday = first_day - timedelta(days=7)
    previous_monday_iso = previous_monday.isocalendar()
    previous_week = previous_monday_iso[1]
    prevous_year = previous_monday_iso[0]

    next_monday = last_day + timedelta(days=1)
    next_monday_iso = next_monday.isocalendar()
    next_week = next_monday_iso[1]
    next_year = next_monday_iso[0]

    return render_template('reports/absences.html',
                           week=week,
                           month=month,
                           year=year,
                           first_day=first_day,
                           last_day=last_day,
                           previous_week=previous_week,
                           prevous_year=prevous_year,
                           next_week=next_week,
                           next_year=next_year,
                           students=students)
