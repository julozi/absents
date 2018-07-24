from flask import Flask
from absents.version import __version__
from absents.views.home import bp_home


app = Flask(__name__)
app.register_blueprint(bp_home)
