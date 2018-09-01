from flask import Blueprint, render_template

bp_reports = Blueprint('reports', __name__)


@bp_reports.route('/general')
def index():
    return render_template('reports/index.html')
