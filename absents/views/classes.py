from flask import Blueprint, render_template, request, url_for

from absents.domain import SchoolClass, Student
from absents.utils import get_closest_school_year

bp_classes = Blueprint('classes', __name__)


@bp_classes.route('')
def list():
    year = int(request.args.get('year', get_closest_school_year()))
    classes = []
    for schoolclass in SchoolClass.query.filter_by(year=year):
        classes.append({
            'name': schoolclass.name,
            'grade': schoolclass.grade + (" (bilingue)" if schoolclass.bilingual else ''),
            'url': url_for('absences.list', class_id=schoolclass.id)})
    ulis_count = Student.query\
                        .join(SchoolClass, Student.schoolclass)\
                        .filter(SchoolClass.year == year)\
                        .filter(Student.ulis == True)\
                        .count()  # noqa
    if ulis_count > 0:
        classes.append({
            'name': "Salle 204",
            'grade': "Tous les niveaux <span class=\"badge badge-secondary\">ULIS</span>",
            'url': url_for('absences.ulis', school_year=year)})
    if len(classes) > 0:
        classes.append({
            'name': "Toutes les classes",
            'grade': "Tous les niveaux",
            'url': url_for('absences.all', school_year=year)
        })
    return render_template('classes/list.html', classes=classes, year=year, ulis=ulis_count > 0)
