from flask import Flask
from absents.version import __version__
from absents.views.classes import bp_classes
from absents.views.home import bp_home


app = Flask(__name__)
app.register_blueprint(bp_home)
app.register_blueprint(bp_classes, url_prefix='/classes')


# Add variable to Jinja context
@app.context_processor
def inject_user():
    return dict(version=__version__)
