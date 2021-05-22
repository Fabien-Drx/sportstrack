from app import db, Gear, Sport, Workout, Track
from datetime import datetime

#  Sports
sport_1 = Sport(id=1, sport='Running')
sport_2 = Sport(id=2, sport='Road Bike')
sport_3 = Sport(id=3, sport='Mountain Bike')
sport_4 = Sport(id=4, sport='Swimming')
sport_5 = Sport(id=5, sport='Openwater Swimming')

#  Gear
gear_1 = Gear(id=1, name='Trabucco', description='2021 Model', purchase_date=datetime.strptime('2021-01-10', '%Y-%m-%d'))
gear_2 = Gear(id=2, name='Look 675', description='My favorite bike', purchase_date=datetime.strptime('2017-04-28', '%Y-%m-%d'))

#  Workout

#  Track

# Add and Commit
db.session.add(sport_1)
db.session.add(sport_2)
db.session.add(sport_3)
db.session.add(sport_4)
db.session.add(sport_5)
db.session.add(gear_1)
db.session.add(gear_2)

db.session.commit()
