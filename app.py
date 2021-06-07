from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.fields.html5 import DateField as html5DateField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gearsports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySupeRsEcretkeY'

db = SQLAlchemy(app)

Bootstrap(app)


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



class SportForm(FlaskForm):
    sport = StringField(label='Sport :', validators=[DataRequired()])
    submit = SubmitField('Add Sport')


class GearForm(FlaskForm):
    name = StringField(label="Gear's name :", validators=[DataRequired()])
    description = StringField(label="Description :", validators=[DataRequired()])
    purchase_date = html5DateField(label="Purchase Date", validators=[DataRequired()])
    submit = SubmitField('Add Gear')


@app.route('/')
def index():
    return render_template("index.html", page_home_active="active")


@app.route('/sports/<action>/<int:id>', methods=['GET', 'POST'])
@app.route('/sports/', methods=['GET', 'POST'])
def sports(action=None, id=-1):

    create_sport_form = SportForm()
    create_sport_form.sport(class_="text_blog")

    if request.method == 'POST' and create_sport_form.validate():
        if action == 'add':
            new_sport = Sport(sport=create_sport_form.sport.data)
            try:
                db.session.add(new_sport)
                db.session.commit()
                action = None
            except exc.IntegrityError:
                db.session.rollback()
                flash('A sport with the same name already exists', 'alert-danger')
        elif action == 'edit':
            edit_sport = Sport.query.get(id)
            edit_sport.sport = create_sport_form.sport.data
            try:
                db.session.commit()
                action = None
            except exc.IntegrityError:
                db.session.rollback()
                flash('A sport with the same name already exists', 'alert-danger')

    if action == 'add':
        create_sport_form.sport.data = ''
    elif action == 'edit':
        create_sport_form.sport.data = Sport.query.get(id).sport

    sports_list = Sport.query.all()
    return render_template('sports.html',
                           sports_list=sports_list,
                           page_sports_active="active",
                           create_sport_form=create_sport_form,
                           action=action)


@app.route('/gears', methods=['GET', 'POST'])
def gears():

    create_gear_form = GearForm()

    if request.method == 'POST' and create_gear_form.validate():
        new_gear = Gear(name=create_gear_form.name.data,
                        description=create_gear_form.description.data,
                        purchase_date=create_gear_form.purchase_date.data)

        try:
            db.session.add(new_gear)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('A gear with the same name already exists', 'alert-danger')

    gears_list = Gear.query.all()
    return render_template('gears.html',
                           gears_list=gears_list,
                           page_gears_active="active",
                           create_gear_form=create_gear_form)


@app.route('/<cat>/<int:id>/delete', methods=['GET', 'POST'])
def delete(cat, id):
    if cat == 'sports':
        to_delete = Sport.query.get(id)
    elif cat == 'gears':
        to_delete = Gear.query.get(id)
    elif cat == 'workouts':
        to_delete = Workout.query.get(id)

    db.session.delete(to_delete)
    db.session.commit()
    flash('Successfully deleted !', 'alert-success')
    return redirect(url_for(cat))

@app.route('/<cat>/<int:id>/edit', methods=['GET', 'POST'])
def edit(cat, id):
    if cat == 'sports':
        obj_to_upd = Sport.query.get(id)
        form = SportForm()
        form.sport.data = obj_to_upd.sport
    elif cat == 'gears':
        obj_to_upd = Gear.query.get(id)
        form = GearForm(obj_to_upd)
    elif cat == 'workouts':
        pass
    else:
        pass

    if request.method == 'POST' and form.validate():
        obj_to_upd.sport = form.sport.data
        db.session.commit()
        return redirect(url_for(cat))


    return render_template('edit.html', form=form)

if __name__ == '__main__':
    app.run()
