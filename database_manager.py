

from model import Event, db
from flask import json

class DatabaseManager:
    def __init__(self, app):
        self.app = app

    def add_event(self, host, message, location, date, budget, dress_code):
        with self.app.app_context():
            Event_info = Event(
                host=host,
                message=message,
                location=location,
                date_going=date,
                dress_code=dress_code,
                budget=budget
            )
            db.session.add(Event_info)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        
    def view_all_event(self):
         #basically when im not working with request and responce i can't access the flask application context so i have to use with app.app_context():
        with self.app.app_context():
                # Fetch information from the database 
                Events_data = Event.query.order_by(Event.date_posted).all()
                # Get all the info and store in a dictionary-like format
                Events_from_db = [message.Eventdb_dict() for message in Events_data]
                # Convert the list of messages to a JSON-formatted string
                json_data = json.dumps(Events_from_db, indent=4)
                return json_data
        
    def view_specific_event(self,id):
         assert isinstance(id, int), "Invalid event ID (not an integer)"
         with self.app.app_context():
                load_event = Event.query.get_or_404(id) 
                json_data = json.dumps(load_event.Eventdb_dict())# Serialize the object's attributes
                return json_data
         
    def update_event(self,id, host, message, location, date, budget, dress_code):
         assert isinstance(id, int), "Invalid event ID (not an integer)"
         with self.app.app_context():
            update_event_section = Event.query.get_or_404(id)
            update_event_section.host= host
            update_event_section.message = message
            update_event_section.location = location
            update_event_section.date_going= date
            update_event_section.budget = budget
            update_event_section.dress_code = dress_code
            db.session.commit()
         
    def delete_event(self,id):
        with self.app.app_context():
            delete_event= Event.query.get_or_404(id)
            db.session.delete(delete_event)
            db.session.commit()
