from calendar import monthrange
from datetime import date, timedelta
from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import and_, or_

from absents import db
from absents.domain import Absence, Grade, SchoolClass, Student, Vacation

bp_absences = Blueprint('absences', __name__)


@bp_absences.route('/<int:class_id>/absences', methods=['GET'])
def list(class_id):
    # TODO: check if class exists
    schoolclass = SchoolClass.query.get(class_id)

    today = date.today()
    try:
        month = int(request.args.get('month', today.month))
    except ValueError:
        month = today.month
    try:
        year = int(request.args.get('year', schoolclass.year))
    except ValueError:
        year = schoolclass.year

    if year < schoolclass.year or year > schoolclass.year + 1:
        year = schoolclass.year if month >= 9 else schoolclass.year + 1

    # august is forbidden
    if month == 8:
        if today.year <= schoolclass.year:
            month = 9
        else:
            month = 7

    # adujst year depending on the month
    if month <= 7 and year != schoolclass.year + 1:
        year = schoolclass.year + 1

    # get first and last day of month
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # generate vacation list and weekend list
    vacations = Vacation.query.filter(or_(and_(Vacation.end_date >= first_day,
                                               Vacation.end_date <= last_day),
                                          and_(Vacation.start_date >= first_day,
                                               Vacation.start_date <= last_day),
                                          and_(Vacation.start_date < first_day,
                                               Vacation.end_date > last_day))
                                      ).all()
    vacation_days = []
    weekend_days = []
    for day in range(1, last_day.day+1):
        d = date(year, month, day)

        if d.isoweekday() in (3, 6, 7):
            weekend_days.append(day)
        else:
            for vacation in vacations:
                if vacation.start_date <= d and vacation.end_date >= d:
                    vacation_days.append(day)
                    break

    # previous and next month
    previous_month = date(year, month, 1) - timedelta(days=1) if first_day > date(schoolclass.year, 9, 1) else None
    next_month = date(year, month, 1) + timedelta(days=last_day.day) if first_day < date(schoolclass.year + 1, 7, 1) else None

    # retrieve students
    students = Student.query.filter_by(schoolclass=schoolclass)\
                            .filter(or_(and_(Student.end_date >= first_day,
                                             Student.end_date <= last_day),
                                        and_(Student.start_date >= first_day,
                                             Student.start_date <= last_day),
                                        and_(Student.start_date < first_day,
                                             Student.end_date > last_day)))\
                            .join(Grade, Student.grade)\
                            .order_by(Grade.cycle, Grade.level, Student.lastname, Student.firstname)\
                            .all()

    # retrieve absences
    absence_objs = Absence.query\
                          .join(Student, Absence.student)\
                          .filter(Student.schoolclass == schoolclass)\
                          .filter(Absence.date >= first_day)\
                          .filter(Absence.date <= last_day)\
                          .all()
    absences = {}
    for student in students:
        absences[student] = {}
        for day in range(1, last_day.day + 1):
            absences[student][day] = None
    for absence in absence_objs:
        absences[absence.student][absence.date.day] = absence

    nb_students = len(students)
    nb_possible_presences = (last_day.day - len(weekend_days) - len(vacation_days)) * 2 * nb_students
    nb_absences = sum([absence.score for absence in absence_objs])
    prc_absences = nb_absences * 100.0 / nb_possible_presences
    prc_presences = 100.0 - prc_absences

    return render_template('absences/list.html',
                           schoolclass=schoolclass,
                           month=month,
                           year=year,
                           previous_month=previous_month,
                           next_month=next_month,
                           last_day=last_day,
                           vacation_days=vacation_days,
                           weekend_days=weekend_days,
                           students=students,
                           absences=absences,
                           nb_students=nb_students,
                           nb_possible_presences=nb_possible_presences,
                           nb_absences=nb_absences,
                           prc_absences=prc_absences,
                           prc_presences=prc_presences)


@bp_absences.route('/<int:class_id>/absences', methods=['POST'])
def create_or_update(class_id):
    d = date(int(request.form['year']), int(request.form['month']), int(request.form['day']))
    absence = Absence.query.filter_by(student_id=int(request.form['student']))\
                           .filter_by(date=d)\
                           .first()

    period = request.form['period']

    if period == "":
        if absence is not None:
            db.session.delete(absence)
    else:
        if absence is None:
            absence = Absence(student_id=int(request.form['student']), date=d)
            db.session.add(absence)
        absence.period = period
        absence.reason = request.form['reason'] if len(request.form['reason']) > 0 else None

    db.session.commit()
    return redirect(url_for('absences.list', class_id=class_id, year=d.year, month=d.month))
