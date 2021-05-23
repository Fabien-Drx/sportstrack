from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gearsports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySupeRsEcretkeY'

db = SQLAlchemy(app)


class SportForm(FlaskForm):
    sport = StringField(label='Sport :', validators=[DataRequired()])
    submit = SubmitField('Add Sport')


class Gear(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), unique=False, index=True)
    purchase_date = db.Column(db.Date, default=datetime.now())
    offset = db.Column(db.Integer(), nullable=False, unique=False, default=0)
    tracks = db.relationship('Track', backref='gear_track', lazy='dynamic')


class Workout(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    workout_date = db.Column(db.Date, default=datetime.now())
    distance = db.Column(db.Float(), default=0)
    avg_pace = db.Column(db.Float(), default=0)
    avg_fc = db.Column(db.Float(), default=0)
    tracks = db.relationship('Track', backref='workout_track', lazy='dynamic')


class Sport(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sport = db.Column(db.String(50), index=True, nullable=False, unique=True)
    workouts = db.relationship('Workout', backref='sport', lazy='dynamic')


class Track(db.Model):
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), primary_key=True)
    gear_id = db.Column(db.Integer, db.ForeignKey('gear.id'), primary_key=True)


@app.route('/')
def index():
    return render_template("index.html", page_home_active="active")


@app.route('/sports', methods=['GET', 'POST'])
def sports():

    create_sport_form = SportForm()

    if request.method == 'POST' and create_sport_form.validate():
        new_sport = Sport(sport=create_sport_form.sport.data)
        try:
            db.session.add(new_sport)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            flash('A sport with the same name already exists', 'alert-danger')
    else:
        if create_sport_form.errors:
            flash(create_sport_form.errors)

    sports_list = Sport.query.all()
    return render_template('sports.html', sports_list=sports_list, page_sports_active="active", create_sport_form=create_sport_form)


@app.route('/gears')
def gears():
    gears_list = Gear.query.all()
    return render_template('gears.html', gears_list=gears_list, page_gears_active="active")


if __name__ == '__main__':
    app.run()
