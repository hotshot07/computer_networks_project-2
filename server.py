# Importing sockets for low level implementation of networks
import socket

# Importing thread to make it a multithreaded application
from threading import Thread

# For handling the CTRL-C input
import sys

# Used for adding the waiting functionality
import time

# Allows us to open website
import webbrowser as wb

# Handling Ctrl+C in a very cool way
import signal

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

# It stores the client and doctor sockets, which are in the chatroom
# This is the MOST IMPORTANT thing that helps maintain a session
clientToDoctor = []

# List to keep track of the threads
threads = []

# The HSE website that user is connected to when he declines to chat with doctor
url = "https://www2.hse.ie/conditions/coronavirus/coronavirus.html"

# Function to handle Ctrl-C


def sigint_handler(signum, frame):
    print('\n Server Shutting down')
    server_socket.close()
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)

# Function to get username of the new user that connects to the server
# ----- FORMAT -----
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


# ---------------------client == patient functions ---------------------

def greetUser(client_socket, username):
    # Greeting our beloved client
    client_socket.send(
        f"Welcome to this helpline {username}!\n".encode('utf-8'))
    client_socket.send(
        f"We have collected your location data\n".encode('utf-8'))
    client_socket.send(
        f"Press Y to begin the survey".encode('utf-8'))


# List of answers that a user can respond to while giving the survey

possibleAnswers = ['y\n', 'yes\n', 'Y\n',
                   'Yes\n', 'n\n', 'no\n', 'N\n', 'No\n']


# Function used to send survey to the clinet
# Has a client_socket and question index value passed to it
# It send the client_socket that particular question

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


# All questions respsonded by the client are stored in answerlist
# which is passed to this function
# Each question has a different weight from which the final score is calculated
# If that score is above a certain threshold, user gets a
def checkForVirus(answerlist):
    weights = [0.88, 0.38, 0.33, 0.18, 0.33, 0.38, 0.14,
               0.14, 0.14, 0.11, 0.05, 0.05, 0.04, -1, 0.3, 0.5, 0.3]

    # First response rejected as it's the asnwer to if you want to start
    # the survey

    answerlist = answerlist[1:]
    virusSum = 0
    affirmitiveAnswers = ['y\n', 'yes\n', 'Y\n',
                          'Yes\n']

    for i in range(len(answerlist)):
        if answerlist[i] in affirmitiveAnswers:
            virusSum = virusSum + weights[i]

    if virusSum >= 1.58:
        return "positive"
    else:
        return "negative"


def sendMessageToDoctor(client_socket, messageDoctor):
    # message consists of username of the client, so doctor
    # knows who is sending the message

    message = (str(clients[client_socket]) +
               " > " + messageDoctor).encode('utf-8')

    for client in clientToDoctor:
        if client != client_socket:
            try:
                client.send(message)
            except:
                print(f"{clients[client_socket]} has left the application")


def askForDoctor(client_socket):
    while True:
        try:

            ans = client_socket.recv(2048)
            ans = ans.decode('utf-8')

            if ans in possibleAnswers:
                if ans not in ['y\n', 'yes\n', 'Y\n',
                               'Yes\n']:
                    client_socket.send(
                        "We are redirecting you to the HSE website for more information as to how to arrange your test".encode('utf-8'))
                    wb.open(url, new=2)
                    client_socket.close()
                else:
                    connectToDoctor(client_socket)
                    client_socket.close()
        except:
            continue


def connectToDoctor(client_socket):

    # check for doctor here
    doctorFound = False

    while not doctorFound:
        for socket in clientToDoctor:
            if clients[socket] == "Doctor":
                doctorFound = True

        if doctorFound == False:
            client_socket.send("Waiting for a doctor... \n".encode('utf-8'))
            time.sleep(5)

    # check for more than 2 users in clientToDoctor list
    session = False
    while not session:
        if len(clientToDoctor) < 2:
            session = True
        else:
            client_socket.send(
                "Doctor is busy... trying again in 5 seconds\n".encode('utf-8'))
            time.sleep(5)

    client_socket.send("You are now connected to a doctor\n".encode('utf-8'))
    client_socket.send("Type 'close' to end this session".encode('utf-8'))

    clientToDoctor.append(client_socket)

    while True:
        try:
            messageDoctor = client_socket.recv(2048)
            messageDoctor = messageDoctor.decode('utf-8')
            if messageDoctor:
                if messageDoctor == 'close\n':
                    print(f"{clients[client_socket]} has left the server")
                    # removing from lists
                    clientToDoctor.remove(client_socket)
                    clientList.remove(client_socket)
                    del clients[client_socket]
                    client_socket.close()
                else:
                    sendMessageToDoctor(client_socket, messageDoctor)
        except:
            continue


# --------------------End of client functions ------------------------------


# ---------------------Start of doctor functions -----------------------------

def sendToClient(message_to_send, client_socket):
    for client in clientToDoctor:
        # Don't send it to from where we receive the message
        if client != client_socket:
            try:
                client.send(message_to_send)
            except:
                print(f"{clients[client]} has left the application")


def doctorThread(client_socket):
    client_socket.send(
        "Welcome to the server Doctor. Thank you for your service".encode('utf-8'))
    while True:
        try:
            message = client_socket.recv(2048)
            message = message.decode('utf-8')
            if message == "doctor exiting":
                print("Doctor has left the server")
                clientToDoctor.remove(client_socket)
                clientList.remove(client_socket)
                del clients[client_socket]
                client_socket.close()
            else:
                message_to_send = ("Doctor" + " > " + message).encode('utf-8')
                sendToClient(message_to_send, client_socket)
        except:
            continue

#------------------End of doctor functions ------------------------------------


def clientThread(client_socket, client_address):

    new_user = getNewUser(client_socket)

    username = new_user['data']

    clients[client_socket] = username

    print(f"{username} has connected to the server")

    #-----------code separates here for doctor and patient -------------------
    if username == "Doctor":
        clientToDoctor.append(client_socket)
        doctorThread(client_socket)

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
                # print(answerlist)
                if question > 16:
                    # we have finished our survey
                    client_socket.send("End of Survey\n".encode('utf-8'))
                    client_socket.send(
                        "We are now checking if you need to be tested\n".encode('utf-8'))

                    confirmation = checkForVirus(answerlist)

                    if confirmation == "positive":
                        client_socket.send(
                            "You will need a test\n Would you like to speak to a doctor?".encode('utf-8'))
                        askForDoctor(client_socket)

                    elif confirmation == "negative":
                        client_socket.send(
                            "You don't need a test\n".encode('utf-8'))
                        print(f"{username} has left the server")
                        client_socket.close()

                sendSurvey(client_socket, question)
                question = question + 1

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
