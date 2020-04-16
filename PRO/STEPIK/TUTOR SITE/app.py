# coding: utf-8

from flask import Flask
from flask import render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from models import Teacher, Goal, Schedule, Booking, Request, init_db
from config import Config
from loads import load_data
from forms import BookingForm, RequestForm
from data import week_days

from random import sample
import os

app = Flask(__name__)
app.config.from_object(Config)

app.jinja_env.add_extension('jinja2.ext.i18n')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

num_teach = 6

db = SQLAlchemy(app)


def get_goals():
    d_goals = {}
    for goal in db.session.query(Goal).all():
        d_goals[goal.goal_id] = goal.name_ru
    return d_goals

@app.errorhandler(404)
def http_404_handler(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index')
@app.route('/profiles/<aim>')
def index(aim=None):
    if aim == None:
        teachers = [t for t in db.session.query(Teacher).order_by(func.random()).limit(num_teach)]
    else:
        teachers = [t for t in db.session.query(Teacher).order_by(func.random())]
    return render_template('index.html', teachers=teachers, aim=aim)

@app.route('/goal/<goal>')
def goal(goal):
    teachers = []
    for t in db.session.query(Teacher).order_by(func.random()):
        if goal in [g.name for g in t.goals]:
            teachers.append(t)
    goal = db.session.query(Goal).filter(Goal.name == goal).first()
    return render_template('goal.html', teachers=teachers, goal=goal)

@app.route('/profile/<teach_id>')
def profile(teach_id):
    l_sched = []
    teach = db.session.query(Teacher).get_or_404(teach_id)
    for s in db.session.query(Schedule).filter(Schedule.teach_id == teach_id).all():
        if s.status == 1:
            d_sched = {'day': s.day, 'time': s.time, 'id': s.time_id}
            l_sched.append(d_sched)
    d_goals = get_goals()
    return render_template('profile.html', teach=teach, schedule = l_sched, week_days=week_days, goals=d_goals)

@app.route('/done', methods=['GET'])
def done_page():
    return render_template('done.html')

@app.route('/booking/<int:sched_id>', methods=['POST', 'GET'])
def booking(sched_id):
    sched = db.session.query(Schedule).filter(Schedule.time_id == sched_id).one()
    teach = db.session.query(Teacher).get_or_404(sched.teach_id)
    form_booking = BookingForm()
    if form_booking.validate_on_submit():
        client_name = form_booking.client_name.data
        client_phone = form_booking.client_phone.data
        teach_id = form_booking.teach_id.data
        book_day = form_booking.book_day.data
        book_time = form_booking.book_time.data  
        book_new = Booking(name=client_name, phone=client_phone, schedule_id=sched.time_id)
        book_new.schedule = sched
        sched.status = 2
        db.session.add(book_new)
        db.session.commit()
        book_data = {'name': client_name, 'phone': client_phone, 'day_name': week_days[sched.day], 'time': form_booking.book_time.data}
        return redirect(url_for('done_page'))
    
    book_data = {'day_name': week_days[sched.day]}
    return render_template('booking.html', teach=teach, book_data=book_data, sched=sched, form_booking=form_booking)

@app.route('/request', methods=['POST', 'GET'])
def req():
    form_request = RequestForm()
    if form_request.validate_on_submit():
        goal = int(form_request.goal.data)
        client_name = form_request.client_name.data
        client_phone = form_request.client_phone.data
        request_new = Request(name=client_name, phone=client_phone, goal_id=goal)
        db.session.add(request_new)
        db.session.commit()
        return redirect(url_for('done_page'))
    return render_template('request.html', form_request=form_request)

if __name__ == "__main__":
    app.run(debug=True)