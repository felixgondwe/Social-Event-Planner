from flask import Flask, flash, redirect, render_template, request, url_for,json
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import Column, Date
import datetime
import socket
import json

FORMAT = "utf-8"
HEADER = 64
socket_server_IP = "192.168.1.236"
socket_server_PORT = 9999
POST_MESSAGE = "POST: "
UPDATE_MESSAGE = "UPDATE: "

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tries to connect the the server with HOST and PORT 
socket_client.connect((socket_server_IP, socket_server_PORT))  

#creates an instance of the flask application 
app = Flask(__name__)

#flask decorator used to define endpoints for web application and /... is the url and HTTP post request 
@app.route("/receive_message", methods = ['POST'])
def send_message():
    data = request.form.get('message')
    host = request.form.get('host')
    location = request.form.get('location')
    date = request.form.get('date')
    budget = request.form.get('budget')
    dress_code = request.form.get('dressCode')
    try: 
        #sending byte messsage to the server 
        c_message = f"{POST_MESSAGE},{data},{host},{location},{date},{budget},{dress_code}".encode(FORMAT)
        c_msg_lenght_send = str(len(c_message)).encode(FORMAT)
        c_msg_lenght_send += b' ' * (HEADER - len(c_msg_lenght_send))
        socket_client.send(c_msg_lenght_send)
        socket_client.send(c_message)
        #Receive and Decode data
        response = socket_client.recv(4096).decode(FORMAT)

        #sending data to frontend so it can be access/desgined 
        return render_template('index.html', response = response)
    except Exception as e: 
        return render_template('index.html', response=f'Error: {str(e)}')
    
@app.route('/all_messages', methods=['GET'])
def all_messages():
        try:
            # Create a "VIEW" command and Send i to the server
            view_command = "VIEW: ".encode(FORMAT)
            msg_length_send = str(len(view_command)).encode(FORMAT)
            msg_length_send += b' ' * (HEADER - len(msg_length_send))
            socket_client.send(msg_length_send)
            socket_client.send(view_command)

            # Receive and decode the data from the server
            received_data = socket_client.recv(4096).decode(FORMAT)
            
            # Parse the JSON data into a Python list
            data = json.loads(received_data)
            
            
            return render_template('all_messages.html', data=data)
        except json.JSONDecodeError as json_error:
            # Handle JSON parsing errors
            return render_template('index.html', response=f'JSON Error: {json_error}')
        except Exception as e: 
            return render_template('index.html', response=f'Error: {str(e)}')#change to data = None then and recall all_message
        
@app.route('/vote/<int:id>', methods=['POST'])
def vote(id):

    user_vote = request.form.get('vote')
    message_id = id
    try:
        vote_command = f"VOTE: ,{message_id},{user_vote}".encode(FORMAT)
        msg_length_send = str(len(vote_command)).encode(FORMAT)
        msg_length_send += b' ' * (HEADER - len(msg_length_send))
        socket_client.send(msg_length_send)
        socket_client.send(vote_command)

        return redirect(url_for('all_messages')) 
    except Exception as e:
        return render_template('index.html', response=f'Error: {str(e)}')

@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
        if request.method == "POST":
            new_message = request.form.get('new_message')
            new_host = request.form.get('new_host')
            new_location = request.form.get('new_location')
            new_date = request.form.get('new_date')
            new_budget = request.form.get('new_budget')
            new_dress_code = request.form.get('new_dressCode')
            update_id = id
            update_command = f"UPDATE: ,{update_id},{new_message},{new_host},{new_location},{new_date},{new_budget},{new_dress_code}".encode(FORMAT)
            msg_length_send = str(len(update_command )).encode(FORMAT)
            msg_length_send += b' ' * (HEADER - len(msg_length_send))
            socket_client.send(msg_length_send)
            socket_client.send(update_command )
            received_data = socket_client.recv(4096).decode(FORMAT)

            return redirect(url_for('all_messages')) 
             
        load_data= f"LOAD: ,{id}".encode(FORMAT)

        msg_length_send = str(len(load_data)).encode(FORMAT)
        msg_length_send += b' ' * (HEADER - len(msg_length_send))
        socket_client.send(msg_length_send)
        socket_client.send(load_data)
        received_data = socket_client.recv(4096).decode(FORMAT)
            
        # Parse the JSON data into a Python list
        data = json.loads(received_data)
    
        return render_template('update.html', message_to_update = data)
    
@app.route("/delete/<int:id>, methods = ['DELETE']")
def delete(id): 
    delete_id = id
    try: 
        delete_data = f"DELETE: ,{delete_id}".encode(FORMAT)
        msg_length_send = str(len(delete_data)).encode(FORMAT)
        msg_length_send += b' ' * (HEADER - len(msg_length_send))
        socket_client.send(msg_length_send)
        socket_client.send(delete_data)
        received_data = socket_client.recv(4096).decode(FORMAT)


        return redirect(url_for('all_messages'), response = received_data) 
    except Exception as e:
        return render_template('all_messages.html', response=f'Error: {str(e)}')
         
    
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)