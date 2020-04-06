# Importing sockets for low level implementation of networks
import socket

# Importing thread to make it a multithreaded application
from threading import Thread

# For handling the CTRL-C input
import sys

# Setting up server_socket to set up TCP/IP and IPv4 protocol and
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Setting up socket options
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# IP and PORT of the socket
IP = "127.0.0.1"
PORT = 42069

# Header length used to receive the username
HEADER_LENGTH = 10

# Binding the socket
server_socket.bind((IP, PORT))

# Listening for new connections
server_socket.listen(100)

# Clients dictionary with client_socket as key, username as data
clients = {}

# List of client_sockets
clientList = []

# List to keep track of the threads
threads = []

# Handling Ctrl+C in a very cool way
import signal


def sigint_handler(signum, frame):
    print('\n Server Shutting down')
    server_socket.close()
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)

# Function to get username of the new user that connects to the server


#----- FORMAT -----
# 4.........Name
def getNewUser(client_socket):
    try:
        # Receiving our "header" containing message length
        message_header = client_socket.recv(HEADER_LENGTH)

        # If we received no data client has closed client_socket and we can return false
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        dataReceived = client_socket.recv(message_length)
        dataReceived = dataReceived.decode('utf-8')
        return {'header': message_header, 'data': dataReceived}

    except:
        return False


def sendSurvey(client_socket, question):

    surveyList = [
        "Do you have a fever? Y/N",
        "Do you have a dry cough? Y/N",
        "Are you coughing up phlegm or mucous? Y/N",
        "Do you have shortness of breath? Y/N",
        "Can you hold your breath for 10 seconds? Y/N",
        "Are you feeling fatigued or exhausted? Y/N",
        "Have you got a sore throat? Y/N",
        "Are you experiencing headaches? Y/N",
        "Are you experiencing muscle aches? Y/N",
        "Are you experiencing chills? Y/N",
        "Have you got nausea/ have you been vomiting? Y/N",
        "Have you had diarrhoea? Y/N",
        "Do you have a stuffy nose? Y/N",
        "Do you have a runny nose? Y/N",
        "Have you been to an affected area in the past two weeks e.g. Spain, Italy, Wuhan? Y/N",
        "Have you been in contact with any people who have tested positive for the virus? Y/N",
        "Have you been to a hospital in the past two weeks? Y/N"]

    client_socket.send(surveyList[question].encode('utf-8'))


def checkForVirus(answerlist):
    weights = [0.88, 0.38, 0.33, 0.18, 0.33, 0.38, 0.14,
               0.14, 0.14, 0.11, 0.05, 0.05, 0.04, -1, 0.3, 0.5, 0.3]
    answerlist = answerlist[1:]
    virusSum = 0
    for i in range(len(answerlist)):
        if answerlist[i] == 'Y\n':
            virusSum = virusSum + weights[i]
            print(virusSum)
            print("\n")

    if virusSum >= 1.58:
        return "positive"
    else:
        return "negative"


def greetUser(client_socket, username):
    # Greeting our beloved client
    client_socket.send(
        f"Welcome to this helpline {username}!\n".encode('utf-8'))
    client_socket.send(
        f"We have collected your location data anonymously\n".encode('utf-8'))
    client_socket.send(
        f"Press Y to begin the survey or N to exit".encode('utf-8'))


possibleAnswers = ['y\n', 'yes\n', 'Y\n',
                   'Yes\n', 'n\n', 'no\n', 'N\n', 'No\n']

# A thread that is made when a new user connects


def clientThread(client_socket, client_address):

    new_user = getNewUser(client_socket)

    username = new_user['data']

    clients[client_socket] = username

    print(f"{username} has connected to the server")

    greetUser(client_socket, username)

    question = 0

    answerlist = []

    # Now check if we got a message
    while True:
        try:
            message = client_socket.recv(2048)
            message = message.decode('utf-8')
            if message in possibleAnswers:
                answerlist.append(message)
                print(answerlist)
                if question > 16:
                    client_socket.send("End of Survey\n".encode('utf-8'))
                    client_socket.send(
                        "We are now checking if you need to be tested\n".encode('utf-8'))

                    confirmation = checkForVirus(answerlist)

                    if confirmation == "positive":
                        client_socket.send(
                            "You will need a test\n".encode('utf-8'))
                        client_socket.close()

                    elif confirmation == "negative":
                        client_socket.send("You're fine\n".encode('utf-8'))
                        client_socket.close()

                sendSurvey(client_socket, question)
                question = question + 1

            if message not in possibleAnswers:
                client_socket.send("Please send a Y/N reply only")

        except:
            continue


# Main Server always running accepting new connections
print("Server is now running")

while True:
    # Accepting the socket and address of the client
    client_socket, client_address = server_socket.accept()

    # Addding client_socket to the list
    clientList.append(client_socket)

    # Creates an individual thread for every user
    process = Thread(target=clientThread, args=[
        client_socket, client_address])

    # If server is closed, kill all the threads
    process.daemon = True

    process.start()
    threads.append(process)

    # Function to remove user from the chatroom
# def removeUser(client_socket):
#     if client_socket in clientList:
#         print(clientList)
#         clientList.remove(client_socket)
#         del clients[client_socket]


# # Function to send messages to all the clients connected to the chat server
# def sendToAll(message, client_socket):
#     for client in clientList:
#         # Don't send it to from where we receive the message
#         if client != client_socket:
#             try:
#                 client.send(message)
#             except:
#                 print(f"{clients[client]} has left the application")
#                 removeUser(client)
