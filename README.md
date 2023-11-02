# Social-Event-Planner

{Python, Flask, CSS, Html, Jinja, SQL, JSON, Powershell}

BACKEND

Python program that combines a Flask web application with a socket-based server for creating, updating, and viewing messages on a message board.
 
Here's a high-level summary of what the code is about:

The code defines a Flask web application that serves as the frontend for interacting with the message board. The web application has several routes for sending, viewing, voting on, updating, and deleting messages.

It uses SQLAlchemy to create and manage a database (SQLite in this case) to store messages on the message board. The database schema is defined by the Board class.

The code also sets up a socket-based server that listens for connections on a specific IP address and port. Clients can connect to this server to send commands and data related to the message board.

The server handles various commands received from clients, such as posting a message, viewing all messages, voting on a message, updating a message, and deleting a message. These commands are received via the socket connection and processed accordingly.

When a message is posted through the web application, it is sent to the server using a socket connection. The server then adds the message to the database.

When viewing all messages, the web application sends a command to the server to fetch all messages from the database, and the server responds with the data in JSON format.

Voting, updating, and deleting messages are also performed through the web application by sending the corresponding commands to the server via the socket connection.

Error handling is in place for various scenarios, and exceptions are caught to prevent crashes.

The code run in local network environment, as it specifies an IP address of '192.168.1.236' and port 9999. However, it is important to note that this code can also function effectively in a wider network context.

The web application is defined using Flask, and templates are used to render pages with data from the server.

Overall, this code combines a web interface and a socket-based server to create a simple message Event system where users can post, view, and interact with messages.

Command-Based Communication: The protocol for communication between the client and server is command-based. Clients send specific commands (e.g., "POST:", "VIEW:", "VOTE:") along with data. The server interprets these commands and takes appropriate actions based on them.



The implementation of TCP (Transmission Control Protocol) in the provided code is an essential part of creating a network-based messaging system. 

Socket Initialization: The code begins by importing the socket module, which is used to create and manage network sockets. It initializes a TCP socket with the line server = socket.socket(socket.AF_INET, socket.SOCK_STREAM). This line creates a TCP socket and associates it with the IPv4 address family (AF_INET) and the SOCK_STREAM socket type, which is designed for reliable, stream-based communication.

Binding and Listening: The server socket is bound to a specific IP address and port using server.bind(ADDR), where ADDR is a tuple containing the IP address and port number. This step associates the server socket with a network interface and port, allowing it to accept incoming connections. The code later initiates listening for incoming connections using server.listen().

Handling Clients: The code uses multithreading to handle multiple clients concurrently. When a client connects, a new thread is created, and the handle_client function is called with the connected socket and client address. This function handles communication with the client. In this way, the server can handle multiple clients simultaneously.

Data Transfer: When clients send messages to the server, they are received using conn.recv(HEADER) to read the message's length and conn.recv(msg_length) to receive the actual message. The received data is decoded using the specified encoding format, which is "utf-8" in this case.

FRONTEND

 frontend code is very user-friendly, easy to navigate, and has a professional and aesthetically pleasing design with nice colors. It also follows responsive design principles, making it suitable for mobile devices. Here are some key points highlighting the user-friendly and professional design aspects:

 Navigation Menu: he navigation menu is well-organized and features a logo with an animated effect, providing a visually appealing and engaging element for users.

 Form Design: The form for creating and updating messages is neatly organized. It uses clear labels for each input field, making it easy for users to understand what information to provide.

 Input Fields: Input fields have a consistent design, with proper placeholder text and clear labels. The design includes a focus effect, making it visually responsive when users interact with the form.

 Buttons: The "Post" and "Update" buttons have a modern design with a hover effect, making them stand out and inviting user interaction.

 Response Messages: The code provides user-friendly response messages, ensuring users receive feedback about the actions they've taken. These messages are displayed in a clear and stylish manner.

 Font Selection: The code imports fonts from Google Fonts (Poppins), which enhances the overall appearance and readability of the text.

 Color Palette: The color scheme is pleasing to the eye, with a combination of black, peachpuff, and white. This color choice ensures readability and a professional look.

 Responsive Design: The code includes responsive design elements, making sure that the website adapts well to various screen sizes, including mobile devices.

