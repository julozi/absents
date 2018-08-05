from flask import Blueprint, render_template, request

from absents.domain import SchoolClass
from absents.utils import get_closest_school_year

bp_classes = Blueprint('classes', __name__)


@bp_classes.route('')
def list():
    year = int(request.args.get('year', get_closest_school_year()))
    classes = SchoolClass.query.filter_by(year=year)
    return render_template('classes/list.html', classes=classes, year=year)
