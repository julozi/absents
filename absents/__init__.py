import locale
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from absents.version import __version__


try:
    locale.setlocale(locale.LC_TIME, "fr_FR")
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

app = Flask(__name__)
app.config.from_object('absents.default_settings.DefaultSettings')
app.config.from_json(os.path.join(os.getcwd(), 'app.json'), silent=False)
db = SQLAlchemy(app)

import absents.cli  # noqa

from absents.views.absences import bp_absences  # noqa
from absents.views.classes import bp_classes  # noqa
from absents.views.home import bp_home  # noqa
from absents.views.students import bp_students  # noqa
app.register_blueprint(bp_home)
app.register_blueprint(bp_absences, url_prefix='/classes')
app.register_blueprint(bp_classes, url_prefix='/classes')
app.register_blueprint(bp_students, url_prefix='/classes')


# Add variable to Jinja context
@app.context_processor
def inject_user():
    return dict(version=__version__)
