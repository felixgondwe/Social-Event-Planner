"""
SQLAlchemy model: Creation of my database table
Represent the structure and schema of data that my application will interact with 
in this case we are interacting with the Model Event


In the Flask-SQLAlchemy framework, these models are instances of the db.Model class.

"""



from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = "Events"

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), unique=True)
    location = db.Column(db.String(80))
    date_going = db.Column(db.String(80))
    dress_code = db.Column(db.String(80))
    budget = db.Column(db.Integer, default=0)
    yes_count = db.Column(db.Integer, default=0)
    no_count = db.Column(db.Integer, default=0)
    date_posted = db.Column(db.Date, default=date.today)

    def Eventdb_dict(self):
        return {
            'id': self.id,
            'host': self.host,
            'message': self.message,
            'yes_count': self.yes_count,
            'no_count': self.no_count,
            'date_posted': self.date_posted.strftime('%Y-%m-%d'),
            'location': self.location,
            'date_going': self.date_going,
            'budget': self.budget,
            'dress_code': self.dress_code
        }
