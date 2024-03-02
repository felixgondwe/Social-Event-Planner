import socket
import threading

HEADER = 64
PORT = 8888
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.236"
ADDR = (SERVER, PORT) #server is the HOST 

#establish a TCP connection 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#AF_INET address family for ipv4 SOCK_STREAM = socket type for TCP 
#associate socket wiht a specific network interface and port
server.bind(ADDR)


# TODO: add type hints      

def handle_client(conn, addr,db_manager,app):
    
    client_id = f"ID: {addr[0]}:{addr[1]}"
    print(f"[NEW CONNECTION] {client_id} connected.")
    connected = True
    while connected:
        try:
            env_length_length = conn.recv(HEADER).decode(FORMAT)  # conn.recv(HEADER) receives the message of size HEADER bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The value received is stored in env_length_length
            if env_length_length:
                env_length_length = int(env_length_length)  # converts the env_length_length from a string to an integer. The received message
                # the server receives the actual message sent by the client. conn.recv(env_length_length) receives the message of size env_length_length bytes from the client, and decode(FORMAT) decodes the received bytes using the specified encoding format (FORMAT, which is "utf-8" in this case). The decoded message is stored in the variable  event_info.
                event_info = conn.recv(env_length_length).decode(FORMAT)
                if  event_info.startswith(DISCONNECT_MESSAGE):
                    connected = False
                elif event_info.startswith("POST: "):
                    #addr for debugging so I see with Ip posted a message 
                    #conn to send response to client 
                    #db_manager can work with wtv database so it's not hard coded losens up the code 
                    # flask app = app 
                    post_event(addr,conn,event_info,db_manager,app) 
                elif event_info.startswith("VIEW: "):
                    load_all_event(conn,db_manager,app) 
                elif event_info.startswith("LOAD: "):
                     load_event(conn, event_info,db_manager,app)
                elif event_info.startswith("UPDATE: "):
                    print("here")
                    update_event(conn, event_info,db_manager,app)
                elif event_info.startswith("DELETE: "):
                    delete_event(conn,event_info,db_manager,app)
                    
                            
                """elif    event_info.startswith("VOTE: "):
                    with app.app_context():
                        vote_part = event_info.split(',')
                        vote, message_id, user_vote = vote_part
                        message = Board.query.get_or_404(message_id)

                        if user_vote == 'yes':
                            if user_voted_yes == False:
                                message.yes_count += 1
                                user_voted_yes = True
                                if user_voted_n
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
                        db.session.commit()"""
        except:
            break

#Dependency Injection helps loosen up the code for testing 
#directly creating a DatabaseManager makes the code tighly coupled 
"""
By injecting the db_manager parameter, you decouple the function from the specific 
database implementation and make it possible to 
provide a mock or test implementation during unit testing. 
This also makes your code more flexible and testable.

"""


def load_all_event(conn,db_manager,app):
    with app.app_context():
        try:
            conn.send(db_manager.view_all_event().encode(FORMAT))
            print(db_manager.view_all_event())
        except Exception as e:
            print(f"Issue: {e}")


def post_event(addr,conn, event_info, db_manager,app):
    with app.app_context():
            event_parts =   event_info.split(',')
            post,event_message,event_host,event_location,event_date,event_budget,event_dress_code = event_parts             
            try: 
                db_manager.add_event(event_host, 
                                           event_message, 
                                           event_location, 
                                           event_date, 
                                           event_budget,
                                           event_dress_code, 
                                           ) 
                conn.send("Message Posted!!!".encode(FORMAT))
                #debugged 
                print(f"[SUCESS] {addr[0]}: POSTED AN EVENT")
            except Exception as e:
                print(f"Error when committing to the database: {e}")
                conn.send("ERROR!!!".encode(FORMAT))            
 

def load_event(conn, event_info,db_manager,app):
    with app.app_context():
            try:
                load_parts = event_info.split(',')
                load, id = load_parts
                conn.send(db_manager.view_specific_event(int(id)).encode(FORMAT))
            except Exception as e:
                print(f"Error: {e}")



def update_event(conn,event_info,db_manager,app):
    with app.app_context():
        try:
            print("here")
            update_part = event_info.split(',')
            update, id, update_message, update_host, update_location, update_date, update_budget, update_dress_code = update_part
            print(update_dress_code)
            db_manager.update_event(int(id),
                                          update_host,
                                          update_message, 
                                          update_location, 
                                          update_date,
                                          update_budget,
                                          update_dress_code)
            conn.send("Updated!!".encode(FORMAT))
        except Exception as e:
            print(f"Error: {e}")

def delete_event(conn, event_info,db_manager,app): 
    with app.app_context(): 
        try: 
            delete_part =   event_info.split(',')
            delete,id = delete_part
            db_manager.delete_event(int(id))
            conn.send("Deleted!!".encode(FORMAT))
        except Exception as e: 
            print(f"Error: {e}")




def start(db_manager,app):
    #listening for clients to connect to the server so it can accept connections 
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # get the obj of the current socket and addr get the list of the client
        thread = threading.Thread(target=handle_client, args=(conn, addr,db_manager,app))  # handle_client, which is responsible for handling communication with the connected client. get the database manager and the flask app from app_server 
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")