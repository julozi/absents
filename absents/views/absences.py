from calendar import monthrange
from datetime import date, timedelta
from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import and_, or_

from absents import db
from absents.domain import Absence, Grade, SchoolClass, Student, Vacation

bp_absences = Blueprint('absences', __name__)


def adjust_month_and_year(month, schoolyear=None):
    if schoolyear is None:
        today = date.today()
        if month <= 8:
            year = today.year - 1
        else:
            year = today.year
    else:
        if month <= 8:
            year = schoolyear + 1
        else:
            year = schoolyear
    if month == 8:
        month = 9 if year <= schoolyear else 7
    return (month, year)


def render_absences_table(title, month, year, school_year, students, absences, show_class=False, group_by_class=True, manage_url=None):
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    today = date.today()
    the_day = None
    if today >= first_day and today <= last_day:
        the_day = today.day

    # generate vacation list and weekend list
    vacations = Vacation.get_between_dates(first_day, last_day)
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

    absences_data = {}
    for student in students:
        absences_data[student] = {}
        for day in range(1, last_day.day + 1):
            absences_data[student][day] = None
    for absence in absences:
        print(absence)
        absences_data[absence.student][absence.date.day] = absence

    nb_students = len(students)
    nb_possible_presences = (last_day.day - len(weekend_days) - len(vacation_days)) * 2 * nb_students
    nb_absences = sum([absence.score for absence in absences])
    prc_absences = nb_absences * 100.0 / nb_possible_presences if nb_possible_presences != 0 else 0
    prc_presences = 100.0 - prc_absences

    # previous and next month
    view_args = request.view_args
    request_args = request.args.to_dict()
    if 'school_year' in request.args:
        request_args['school_year'] = school_year
    previous_month = date(year, month, 1) - timedelta(days=1) if first_day > date(school_year, 9, 1) else None
    previous_url = None
    if previous_month is not None:
        request_args['month'] = previous_month.month
        values = {**view_args, **request_args}
        previous_url = url_for(request.endpoint, **values)
    next_month = date(year, month, 1) + timedelta(days=last_day.day) if first_day < date(school_year + 1, 7, 1) else None
    next_url = None
    if next_month is not None:
        request_args['month'] = next_month.month
        values = {**view_args, **request_args}
        next_url = url_for(request.endpoint, **values)

    return render_template('absences/list.html',
                           title=title,
                           manage_url=manage_url,
                           show_class=show_class,
                           group_by_class=group_by_class,
                           month=month,
                           year=year,
                           the_day=the_day,
                           previous_month=previous_month,
                           previous_url=previous_url,
                           next_month=next_month,
                           next_url=next_url,
                           last_day=last_day,
                           vacation_days=vacation_days,
                           weekend_days=weekend_days,
                           students=students,
                           absences=absences_data,
                           nb_students=nb_students,
                           nb_possible_presences=nb_possible_presences,
                           nb_absences=nb_absences,
                           prc_absences=prc_absences,
                           prc_presences=prc_presences)


@bp_absences.route('/all/absences', methods=['GET'])
def all():
    today = date.today()
    title = 'Tous les élèves'

    month = int(request.args.get('month', today.month))
    school_year = int(request.args.get('school_year', today.year))
    (month, year) = adjust_month_and_year(month, school_year)

    # get first and last day of month
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # retrieve students
    students = Student.query\
                      .filter(or_(and_(Student.end_date >= first_day,
                                       Student.end_date <= last_day),
                                  and_(Student.start_date >= first_day,
                                       Student.start_date <= last_day),
                                  and_(Student.start_date < first_day,
                                       Student.end_date > last_day)))\
                      .join(Grade, Student.grade)\
                      .order_by(Student.lastname, Student.firstname)\
                      .all()

    # retrieve absences
    absences = Absence.query\
                      .join(Student, Absence.student)\
                      .filter(Absence.date >= first_day)\
                      .filter(Absence.date <= last_day)\
                      .all()

    return render_absences_table(title=title,
                                 month=month,
                                 year=year,
                                 school_year=school_year,
                                 students=students,
                                 absences=absences,
                                 show_class=True,
                                 group_by_class=False)


@bp_absences.route('/ulis/absences', methods=['GET'])
def ulis():
    today = date.today()
    title = 'ULIS'

    month = int(request.args.get('month', today.month))
    school_year = int(request.args.get('school_year', today.year))
    (month, year) = adjust_month_and_year(month, school_year)

    # get first and last day of month
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # retrieve students
    students = Student.query\
                      .join(Grade, Student.grade)\
                      .filter(Student.ulis == True)\
                      .filter(or_(and_(Student.end_date >= first_day,
                                       Student.end_date <= last_day),
                                  and_(Student.start_date >= first_day,
                                       Student.start_date <= last_day),
                                  and_(Student.start_date < first_day,
                                       Student.end_date > last_day)))\
                      .order_by(Grade.cycle, Grade.level, Student.lastname, Student.firstname)\
                      .all()  # noqa

    # retrieve absences
    absences = Absence.query\
                      .join(Student, Absence.student)\
                      .filter(Student.ulis == True)\
                      .filter(Absence.date >= first_day)\
                      .filter(Absence.date <= last_day)\
                      .all()  # noqa

    return render_absences_table(title=title,
                                 month=month,
                                 year=year,
                                 school_year=school_year,
                                 students=students,
                                 absences=absences)


@bp_absences.route('/<class_id>/absences', methods=['GET'])
def list(class_id):
    today = date.today()
    schoolclass = SchoolClass.query.get(class_id)
    title = schoolclass.name

    month = int(request.args.get('month', today.month))
    school_year = schoolclass.year
    (month, year) = adjust_month_and_year(month, school_year)

    # get first and last day of month
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    # retrieve students
    students = Student.query\
                      .join(Grade, Student.grade)\
                      .filter(Student.schoolclass == schoolclass)\
                      .filter(or_(and_(Student.end_date >= first_day,
                                       Student.end_date <= last_day),
                                  and_(Student.start_date >= first_day,
                                       Student.start_date <= last_day),
                                  and_(Student.start_date < first_day,
                                       Student.end_date > last_day)))\
                      .order_by(Student.lastname, Student.firstname)\
                      .all()  # noqa

    # retrieve absences
    absences = Absence.query\
                      .join(Student, Absence.student)\
                      .filter(Student.schoolclass == schoolclass)\
                      .filter(Absence.date >= first_day)\
                      .filter(Absence.date <= last_day)\
                      .all()  # noqa

    return render_absences_table(title=title,
                                 month=month,
                                 year=year,
                                 school_year=school_year,
                                 students=students,
                                 absences=absences,
                                 manage_url=url_for('students.list', class_id=schoolclass.id))


@bp_absences.route('/all/absences', methods=['POST'])
def create_or_update():
    d = date(int(request.form['year']), int(request.form['month']), int(request.form['day']))
    absence = Absence.query.filter_by(student_id=int(request.form['student']))\
                           .filter_by(date=d)\
                           .first()

    period = request.form['period']
    reason = request.form['reason']

    if period == "" and reason == "" :
        if absence is not None:
            db.session.delete(absence)
    else:
        if absence is None:
            absence = Absence(student_id=int(request.form['student']), date=d)
            db.session.add(absence)
        absence.period = period if len(period) > 0 else None
        absence.reason = reason if len(reason) > 0 else None

    db.session.commit()
    return redirect(request.form['next'])
