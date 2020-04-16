# coding: utf-8
from os import curdir
from os.path import join, abspath

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


Base = declarative_base()

db_name = 'Base'

db_name = db_name + '.db'
db_path = 'sqlite:///' + join(abspath(curdir), db_name)
engine = create_engine(db_path)


teach_goal = Table('teach_goals', Base.metadata,
    Column('teach_id', Integer, ForeignKey('teachers.teach_id')),
    Column('goal_id', Integer, ForeignKey('goals.goal_id'))
)
  
class Teacher(Base):
    __tablename__ = 'teachers'
    teach_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    about = Column(String)
    rating = Column(Float, default=5.0)
    picture = Column(String)
    price = Column(Float)
    goals = relationship("Goal", secondary=teach_goal, back_populates="teachers")
    schedules = relationship("Schedule", back_populates="teach")

class Goal(Base):
    __tablename__ = 'goals'
    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    name_ru = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    teachers = relationship("Teacher", secondary=teach_goal, back_populates="goals")
    requests = relationship("Request", back_populates="goal")

class Schedule(Base):
    __tablename__ = 'schedules'
    time_id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String)
    time = Column(String)
    status = Column(Integer)
    teach_id = Column(Integer, ForeignKey("teachers.teach_id"))
    teach = relationship("Teacher", back_populates="schedules")
    booking = relationship("Booking", back_populates="schedule")

class Booking(Base):
    __tablename__ = 'bookings'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.time_id'))
    schedule = relationship("Schedule", back_populates="booking")
    time_reg = Column(DateTime(timezone=False), default=func.now())

class Request(Base):
    __tablename__ = 'requests'
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    time_reg = Column(DateTime(timezone=True), default=func.now())
    goal_id = Column(Integer, ForeignKey("goals.goal_id"))
    goal = relationship("Goal", back_populates="requests")
    study_time = Column(String)


def init_db():
    Base.metadata.create_all(engine)