import os
from loads import load_data
from models import init_db

class Config(object):
    DB = 'Base.db'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Base.db'

if not os.path.exists(Config.DB):
        init_db()
        load_data()