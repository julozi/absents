from flask import Blueprint, render_template, request

from absents.domain import SchoolClass

bp_classes = Blueprint('classes', __name__)


@bp_classes.route('/')
def list():
    year = request.args.get('year', 2018)
    classes = SchoolClass.query.filter_by(year=year)
    return render_template('classes/list.html', classes=classes)
