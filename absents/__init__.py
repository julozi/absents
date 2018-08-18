import locale
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import url_decode

from absents.version import __version__


try:
    locale.setlocale(locale.LC_TIME, "fr_FR")
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_TIME, "fr_FR.utf8")


# Compliante with https://fr.slideshare.net/landlessness/teach-a-dog-to-rest
# See http://flask.pocoo.org/snippets/38/
class MethodRewriteMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'method' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('method')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)
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
