
from flask import Flask
from model import db
from database_manager import DatabaseManager
from socket_handler import start

app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

#db is the SQL Alchemy database object thats created 
# initialize and configure the database connection for Flask.
db.init_app(app)
#Instance of the Database manager class 
event_db_manager = DatabaseManager(app)

if __name__ == "__main__":
    with app.app_context():
        print("[STARTING] Server is starting...")
        start(event_db_manager,app)

"""
Separation of Concerns: Divide your code into separate modules or classes, 
each with a specific responsibility.

Persistence layer
Database mananger: handles interaction with database -> databae_manager.py 
SQLAlchemy model: creation of the event model -> model.py 

Business layer: 
business logic related to managing events, such as creating, viewing, updating, and deleting events.
database_manager.py 

The key distinction is that the persistence layer primarily deals with data storage and retrieval, 
while the business layer focuses on the application's core logic and rules.

Communication layer/ Network layer 
handles network communication and is responsible for sending and receiving data over a network. 
Socket handing module:  handling network socket connections for the application 
                        responsible for client_server communication 
                        allows the client to communicate with the server through a network connection 
                        Multithreading:

                        The server is capable of handling multiple clients concurrently through the use of multithreading.
                        Each connected client is managed in a separate thread, 
                        allowing the server to accept and process connections from multiple clients simultaneously.
-> socket_handler.py 
Presentation Layer: 
It defines routes, handles HTTP requests, and manages the interaction with the client. 
This part of your application is responsible for handling user interactions,
rendering templates, and sending and receiving data between the client and the server. 
app.py 

database-related operations, another for socket handling, and one for your Flask application.
This separation makes it easier to change or extend each part independently.

"""