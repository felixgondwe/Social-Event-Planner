import socket
import threading

from flask import Flask, flash, json, redirect, render_template, request, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date
import datetime
import socket


app = Flask(__name__)
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app) 


class Board(db.Model):

    __tablename__ = "board"


    id = db.Column(db.Integer, primary_key = True)
    host = db.Column(db.String(20), nullable = False)
    message = db.Column(db.String(200), unique = True)
    location = db.Column(db.String(80))
    date_going = db.Column(db.String(80))
    dress_code = db.Column(db.String(80))
    budget= db.Column(db.Integer, default = 0)
    yes_count = db.Column(db.Integer, default = 0)
    no_count = db.Column(db.Integer, default = 0)
    date_posted = db.Column(Date, default = datetime.date.today)
   

    def Boarddb_dict(self):
        return {
            'id': self.id,
            'host': self.host,
            'message': self.message,
            'yes_count': self.yes_count,
            'no_count': self.no_count,
            'date_posted': self.date_posted.strftime('%Y-%m-%d'),
            'location': self.location,
            'date_going':self.date_going,
            'budget':self.budget,
            'dress_code':self.dress_code
        }

    def __repr__(self):
        return f"{self.id}-{self.message}"
    

POST_MESSAGE_COMMAND = "POST:"
HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.236"
ADDR = (SERVER, PORT) #server is the HOST 

#establish a TCP connection 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#AF_INET address family for ipv4 SOCK_STREAM = socket type for TCP 
#associate socket wiht a specific network interface and port
server.bind(ADDR)


def handle_client(conn, addr):
    
    client_id = f"ID: {addr[0]}:{addr[1]}"
    print(f"[NEW CONNECTION] {client_id} connected.")
    connected = True
    user_voted_no = False
    user_voted_yes = False
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)  # conn.recv(HEADER) receives the message of size HEADER bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The value received is stored in msg_length
            if msg_length:
                msg_length = int(
                    msg_length)  # converts the msg_length from a string to an integer. The received message
                msg = conn.recv(msg_length).decode(FORMAT)
                      # the server receives the actual message sent by the client. conn.recv(msg_length) receives the message of size msg_length bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The decoded message is stored in the variable msg.
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                elif msg.startswith(POST_MESSAGE_COMMAND):
                    try:
                        msg_parts = msg.split(',')
                        post,s_data,s_host,s_location,s_date,s_budget,s_dress_code = msg_parts
                        with app.app_context():
                            #adding data sent from client to my db 
                            board_message_db = Board(host=s_host, message=s_data, location = s_location, date_going=s_date, dress_code = s_dress_code, budget=s_budget )
                            db.session.add(board_message_db)
                            try:
                                #commit data
                                db.session.commit()
                                print(f"{client_id}: Data: {s_data} Host: {s_host}")
                                conn.send("Message Posted!!!".encode(FORMAT))
                            except Exception as e:
                                #that is used to undo or roll back any changes made within the current database session.
                                db.session.rollback()
                                print(f"Error when committing to the database: {e}")
                                conn.send("ERROR!!!".encode(FORMAT))
                                
                    except Exception as e:
                        print(f"Error when committing to the database: {e}") 
                elif msg.startswith("VIEW: "):
                    #basically when im not working with request and responce i can't access the flask application context so i have to use with app.app_context():
                    with app.app_context():
                        try:
                            #featch Information in my db 
                            board_data = Board.query.all()
                            #gets all the info and store in a a dictionary like format
                            v_messages = [message_v.Boarddb_dict() for message_v in board_data]
                            #converts teh list of messages to json-formatted string and json.dump prepares data to be sent over a network 
                            json_data = json.dumps(v_messages, indent = 4)
                            #json_data (which is a JSON-formatted string) over a network connection using send form conn
                            conn.send(json_data.encode(FORMAT))
                            print(json_data)
                        except Exception as e:
                            print(f"Issue: {e}")
                elif msg.startswith("VOTE: "):
                    with app.app_context():
                        vote_part = msg.split(',')
                        vote, message_id, user_vote = vote_part
                        message = Board.query.get_or_404(message_id)

                        if user_vote == 'yes':
                            if user_voted_yes == False:
                                message.yes_count += 1
                                user_voted_yes = True
                                if user_voted_no:
                                    message.no_count -= 1
                                    user_voted_no = False
                            else:
                                print("error: Already voted 'yes'")
                        elif user_vote == 'no':
                            if user_voted_no == False:
                                message.no_count += 1
                                user_voted_no = True
                                if user_voted_yes:
                                    message.yes_count -= 1
                                    user_voted_yes = False
                            else:
                                print("error: Already voted 'no'")
                        else:
                            print("error: Invalid vote option")
                        db.session.commit()
                elif msg.startswith("LOAD: "):
                    load_part = msg.split(',')
                    load, load_id = load_part
                    Load_specific_message(conn,load_id)
                elif msg.startswith("UPDATE: "): 
                    update_part = msg.split(',')
                    update, message_update_id, update_message, update_host, update_location, update_date,update_budget,update_dress_code= update_part
                    Update_specific_message(conn,message_update_id,update_host,update_message,update_location, update_date,update_budget,update_dress_code)
                elif msg.startswith("DELETE: "): 
                    delete_part = msg.split(',')
                    delete,delete_id = delete_part
                    Delete_specific_message(conn,delete_id)
        except:
            break
        

def Load_specific_message(conn, id):
    with app.app_context():
            try:
                load_this = Board.query.get_or_404(int(id))  # Convert ID to integer
                json_data_p = json.dumps(load_this.Boarddb_dict())  # Serialize the object's attributes
                conn.send(json_data_p.encode(FORMAT))
            except Exception as e:
                            print(f"Error: {e}")
def Update_specific_message(conn, id, host, message, location, date,budget, dress_code):
    with app.app_context():
        try:
            update_this = Board.query.get_or_404(id)
            update_this.host= host
            update_this.message = message
            update_this.location = location
            update_this.date_going= date
            update_this.budget = budget
            update_this.dress_code = dress_code
            db.session.commit()
            conn.send("Updated!!".encode(FORMAT))
        except Exception as e:
            print(f"Error: {e}")
def Delete_specific_message(conn, id): 
    with app.app_context(): 
        try: 
            delete_this_message = Board.query.get_or_404(id)
            db.session.delete(delete_this_message)
            conn.send("Deleted!!".encode(FORMAT))
            db.session.commit()
        except Exception as e: 
            print(f"Error: {e}")

def start():
    #listening for clients to connect to the server so it can accept connections 
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # get the obj of the current socket and addr get the list of the client
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # handle_client, which is responsible for handling communication with the connected client.
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



if __name__ == "__main__":
    with app.app_context():
        print("[STARTING] Server is starting...")
        start()
        app.run(host='192.168.1.236', port=9999)
