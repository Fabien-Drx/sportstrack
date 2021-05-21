from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gearsports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Gear(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), unique=False, index=True)
    purchase_date = db.Column(db.Date, default=datetime.now())
    offset = db.Column(db.Integer(), nullable=False, unique=False, default=0)
    tracks = db.relationship('Track', backref='track', lazy='dynamic')


class Workout(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    workout_date = db.Column(db.Date, default=datetime.now())
    distance = db.Column(db.Float(), default=0)
    avg_pace = db.Column(db.Float(), default=0)
    avg_fc = db.Column(db.Float(), default=0)
    tracks = db.relationship('Track', backref='track', lazy='dynamic')


class Sport(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sport = db.Column(db.String(50), index=True, nullable=False, unique=True)
    workouts = db.relationship('Workout', backref='sport', lazy='dynamic')


class Track(db.Model):
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), primary_key=True)
    gear_id = db.Column(db.Integer, db.ForeignKey('gear.id'), primary_key=True)


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
