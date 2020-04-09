# Importing sockets for low level implementation of networks
import socket

# Importing select to poll between the user input and received message
import select

# Getting input from terminal and writing output to terminal
import sys

# creating the client_socket object and adding the TCP/IP and IPv4 protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP and PORT of the socket
IP = "127.0.0.1"
PORT = 42069

# Header length used to receive the username
HEADER_LENGTH = 10

# Let's connect to the server!
client_socket.connect((IP, PORT))


# Handling Ctrl+C in a very cool way
import signal


def sigint_handler(signum, frame):
    print('\n Disconnecting from server')
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)

# Getting the input of username
my_username = input("Username: ")

# Clever function to send username to the server
# Format
# Header: length_of_username
# Body: Username


def sendUsernameToServer(my_username):
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)


# Using the above function
sendUsernameToServer(my_username)

# polling between user input and message received from the server
sockets_list = [sys.stdin, client_socket]

while True:
    # checking for I/O in read_sockets
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socket in read_sockets:
        # If socket == client_socket, we got a message
        if socket == client_socket:
            message = socket.recv(2048)
            if not len(message):
                print("Connection closed by server")
                sys.exit()

            print(message.decode('utf-8'))

        else:
            # Else, we can send a message
            message = sys.stdin.readline()
            message = message.encode('utf-8')
            client_socket.send(message)
            #sys.stdout.write(str(my_username) + " > ")
            # sys.stdout.write(message.decode('utf-8'))
            sys.stdout.flush()


client_socket.close()
