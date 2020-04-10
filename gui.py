import tkinter as tk    # Import tkinker for GUI creation
from PIL import Image, ImageTk  # Allow images to be used as backgrounds
import socket   # Importing sockets for low level implementation of networks
import select   # Importing select to poll between the user input and received message
import sys  # Getting input from terminal and writing output to terminal

# Size of GUI
HEIGHT = 714
WIDTH = 1000

root = tk.Tk()  #Define root to begin window

def sigint_handler(signum, frame):
    print('\n Disconnecting from server')
    sys.exit()

# creating the client_socket object and adding the TCP/IP and IPv4 protocol
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP and PORT of the socket
IP = "127.0.0.1"
PORT = 42069

# Let's connect to the server!
client_socket.connect((IP, PORT))


# Handling Ctrl+C in a very cool way
import signal


signal.signal(signal.SIGINT, sigint_handler)

# Clever function to send username to the server
# Format
# Header: length_of_username
# Body: Username

# Header length used to receive the username
HEADER_LENGTH = 10

def sendUsernameToServer(username_entry):
    username = username_entry.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username)
    checkIO()

def checkIO():
    # polling between user input and message received from the server
    sockets_list = [sys.stdin, client_socket]

    # checking for I/O in read_sockets
    read_sockets, write_socket, error_socket = select.select(
        sockets_list, [], [])

    for socket in read_sockets:
        # If socket == client_socket, we got a message
        if socket == client_socket:
            message = socket.recv(2048)
            if not len(message):
                text_label['text'] = "Connection closed by server"
                print("Connection closed by server")
                sys.exit()
                
            text_label['text'] = message.decode('utf-8')
            print(message.decode('utf-8'))

def sendY():
    # Else, we can send a message
    message = 'y'
    message = message.encode('utf-8')
    client_socket.send(message)
    #sys.stdout.write(str(my_username) + " > ")
    # sys.stdout.write(message.decode('utf-8'))
    sys.stdout.flush()
    checkIO()
    
def sendN():
    # Else, we can send a message
    message = 'n'
    message = message.encode('utf-8')
    client_socket.send(message)
    #sys.stdout.write(str(my_username) + " > ")
    # sys.stdout.write(message.decode('utf-8'))
    sys.stdout.flush()
    checkIO()

    #client_socket.close()

#-----------------------------------------------------
#-------------GUI-LAYOUT------------------------------
#-----------------------------------------------------

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='background.gif')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

covid_label = tk.Label(root, text="COVID-19 Helper", bg="sky blue")
covid_label.config(font=("Arial", 40))
covid_label.place(relx=0.12, rely=0.1, relwidth=0.76, relheight=0.1)

main_frame = tk.Frame(root, bg="light blue")
main_frame.place(relx=0.12, rely=0.2, relwidth=0.76, relheight=0.7)

#----------------------------------------------------------

right_frame = tk.Frame(main_frame, bg="sky blue")
right_frame.place(relx=0.74, rely=0.05, relwidth=0.23, relheight=0.9)

heat_button = tk.Button(right_frame, text="View HeatMap",  bg="deep sky blue", activebackground="steel blue")
heat_button.place(relx=0.05, rely=0.04, relwidth=0.9, relheight=0.2)

info_button = tk.Button(right_frame, text="Covid-19 HSE Info",  bg="deep sky blue", activebackground="steel blue")
info_button.place(relx=0.05, rely=0.28, relwidth=0.9, relheight=0.2)

contact_button = tk.Button(right_frame, text="Heathcare Contacts",  bg="deep sky blue", activebackground="steel blue")
contact_button.place(relx=0.05, rely=0.52, relwidth=0.9, relheight=0.2)

doctor_button = tk.Button(right_frame, text="Speak with a doctor",  bg="orange2", activebackground="DarkOrange1")
doctor_button.place(relx=0.05, rely=0.76, relwidth=0.9, relheight=0.2)

#----------------------------------------------------------

left_frame = tk.Frame(main_frame, bg="sky blue")
left_frame.place(relx=0.03, rely=0.05, relwidth=0.69, relheight=0.9)

text_frame = tk.Frame(left_frame, bg="ghost white")
text_frame.place(relx=0.05, rely=0.05, relwidth= 0.9, relheight=0.6)

text_label = tk.Label(text_frame, bg="ghost white", font=('Courier', 10))
text_label['text'] = "Please enter your username and click\n'Connect to testing server'"
text_label.place(relwidth=1, relheight=1)

server_button = tk.Button(left_frame, text="Connect to testing server",  bg="deep sky blue", activebackground="steel blue", command=lambda: sendUsernameToServer(username_entry.get()))
server_button.place(relx=0.05, rely=0.7, relwidth=0.9, relheight=0.05)

username_label = tk.Label(left_frame, text="Username:", bg="DarkSeaGreen1")
username_label.place(relx=0.05, rely=0.77, relwidth=0.2, relheight=0.05)

username_entry = tk.Entry(left_frame, bg="PaleGreen1")
username_entry.place(relx=0.3, rely=0.77, relwidth=0.65, relheight=0.05)

yes_button = tk.Button(left_frame, text="Yes",  bg="deep sky blue", activebackground="steel blue", command=lambda: sendY())
yes_button.place(relx=0.05, rely=0.84, relwidth=0.44, relheight=0.12)

no_button = tk.Button(left_frame, text="No",  bg="deep sky blue", activebackground="steel blue", command=lambda: sendN())
no_button.place(relx=0.51, rely=0.84, relwidth=0.44, relheight=0.12)

#----------------------------------------------------------

root.mainloop()