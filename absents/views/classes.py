from flask import Blueprint, render_template

bp_classes = Blueprint('classes', __name__)


@bp_classes.route('/')
def list():
    return render_template('classes/list.html')
