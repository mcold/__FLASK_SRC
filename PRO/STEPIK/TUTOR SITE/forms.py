from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class BookingForm(FlaskForm):
    client_name = StringField('client_name', validators=[DataRequired()])
    client_phone = StringField('client_phone', validators=[DataRequired()])
    teach_id = HiddenField('teach_id')
    teach_name = HiddenField('teach_name')
    book_day = HiddenField('book_day')
    book_time = HiddenField('book_time')
    submit = SubmitField('Записаться на пробный урок')

class RequestForm(FlaskForm):
    goal = RadioField('goal', choices=[('1', 'Для путешествий'), ('2', 'Для учебы'), ('3', 'Для работы'),
                                       ('4', 'Для переезда')], validators=[DataRequired()])
    hours = RadioField('hours', choices=[('1-2', '1-2 часа в неделю'), ('3-5', '3-5 часов в неделю'),
                                        ('5-7', '5-7 часов в неделю'), ('7-10', '7-10 часов в неделю')], validators=[DataRequired()])
    client_name = StringField('client_name', validators=[DataRequired()])
    client_phone = StringField('client_phone', validators=[DataRequired()])
    submit = SubmitField('Найдите мне преподавателя')