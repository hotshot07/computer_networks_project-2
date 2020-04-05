#allows creating sockets within our program:
import socket
#each client is going to be a thread:
from _thread import *
#clients look for new providers after time:
import time
#in case server stops:
import sys

serverName = ''
serverPort = 2112

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allows sockets to reuse addresses so that new ones don't need to be
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind() assigns the port number serverPort to the server’s socket.
serverSocket.bind((serverName, serverPort))
print ('\n** SERVER **')

# server listening to new connections
serverSocket.listen()

#list of clients ip addresses
clients=[]

#each thread is a client that connected to the server
def clientthread(conn):
    #send welcome to client
    conn.send(('Welcome').encode())
    conn.send(('Would you like to take a test? (Y/N)').encode())
    answer = conn.recv(2048)

    if (str(answer)[2:-1]=="N"):
        print("N")
        #action
    elif (str(answer)[2:-1]=="Y"):
        print("Y")
        #action
    else:
        print("?")


        
while True:
    
        #if server stops -> all clients stop
    try:

        conn, addr = serverSocket.accept()
            #with this message we also get client's address (useful)
        hello = conn.recv(2048)

            #if client wants to exit
        if hello== ('Client exiting').encode():
            #print('\n** Client ' + str(clientAddress[1]) + ' exited **')

                #remove client from clients list
            clients.remove(conn)
        
        else:
                #when receiving smth from client, if client is already a client, don't call thread again
            if conn not in clients:
                print('\n' + str(hello)[2:-1])
                
                    #add client to list of clients
                clients.append(conn)

                start_new_thread(clientthread, (conn, ))
         
    
    except KeyboardInterrupt:
            #send message to all clients warning that server stopped
        for i in clients:
            i.send(('Server exiting').encode())
        #print('** Server closed **')
        serverSocket.close()
        sys.exit()