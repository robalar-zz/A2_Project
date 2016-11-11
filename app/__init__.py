from flask import Flask

import os

path = os.path.dirname(os.path.realpath(__file__))

if path.find('library.zip') >=0:
    pos = path.find('library.zip')
    path = path[:pos]
    app = Flask(__name__, static_folder=path+'app/static', template_folder=path+'app/templates')
else:
    app = Flask(__name__)

app.config.from_object('config')

from app import views
