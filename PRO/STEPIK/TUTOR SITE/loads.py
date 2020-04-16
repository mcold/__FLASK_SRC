# coding: utf-8

from os import curdir, sep
from os.path import join, abspath

from json import dump, load
import codecs
from models import Goal, Teacher, Schedule, Booking, Request

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

db_name = 'Base.db'

db_path = 'sqlite:///' + join(abspath(curdir), db_name)
engine = create_engine(db_path)


teach_data = load(codecs.open(join(abspath(curdir), 'src' + sep + 'teachers.json'), 'r', 'utf8'))
goals = load(codecs.open(join(abspath(curdir), 'src' + sep + 'goals.json'), 'r', 'utf8'))
emojis = {'travel': '⛱', 'study': '🏫', 'work': '🏢', 'relocate': '🚜'}


def load_schedule(session, teacher, d_sched):
    """
        Load teacher schedule
    """
    for day, d_time in d_sched.items():
        for study_time, activity in d_time.items():
            sched = Schedule(day=day, time=study_time, status=activity, teach_id=teacher.teach_id)
            teacher.schedules.append(sched)
            session.add(sched)            

def load_goals(session):
    """
        Load goals
    """
    for name, name_ru in goals[0].items():
        g = Goal(name = name, name_ru = name_ru, emoji = emojis[name])
        session.add(g)

def get_goal(session, name):
    """
        Get goal by name
    """
    g = session.query(Goal).filter(Goal.name == name).one()
    return g

def load_teach(session):
    """
        Load teachers
    """
    for teach in teach_data:
        t = Teacher(teach_id = teach['id'], name = teach['name'], about = teach['about'], rating = teach['rating'], picture = teach['picture'], price = teach['price'])
        for goal in teach['goals']:
            g = get_goal(session, goal)
            t.goals.append(g)
        load_schedule(session, t, teach['free'])
        session.add(t)

def load_data():
    """
        Load full data
    """
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    session = Session()
    load_goals(session)
    load_teach(session)

    session.commit()
