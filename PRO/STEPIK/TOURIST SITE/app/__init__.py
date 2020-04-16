# coding: utf-8

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config['SECRET_KEY'] = '<replace with a secret key>'

app.jinja_env.add_extension('jinja2.ext.i18n')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


from app import routes