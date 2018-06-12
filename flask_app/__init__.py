from flask import Flask
import os
from config import basedir

flask_app = Flask(__name__)
flask_app.config.from_object('config')

from flask_app import views
