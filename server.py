#allows creating sockets within our program:
import socket
#each client is going to be a thread:
from _thread import *
#clients look for new providers after time:
import time
#in case server stops:
import sys

serverPort = 2112

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind() assigns the port number serverPort to the server’s socket.
serverSocket.bind(('', serverPort))
print ('\n** SERVER **')

#list of clients ip addresses
clients=[]

#each thread is a client that connected to the server
def clientthread(clientAddress):
    #send welcome to client
    serverSocket.sendto(('Welcome').encode(), clientAddress)
    serverSocket.sendto(('Would you like to take a test? (Y/N)').encode(), clientAddress)
    answer, clientAddress = serverSocket.recvfrom(2048)

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
            #with this message we also get client's address (useful)
        hello, clientAddress = serverSocket.recvfrom(2048)

            #if client wants to exit
        if hello== ('Client ' + str(clientAddress[1]) + ' exiting').encode():
            #print('\n** Client ' + str(clientAddress[1]) + ' exited **')

                #remove client from clients list
            clients.remove(clientAddress)
        
        else:
                #when receiving smth from client, if client is already a client, don't call thread again
            if clientAddress not in clients:
                print('\n' + str(hello)[2:-1])
                
                    #add client to list of clients
                clients.append(clientAddress)

                start_new_thread(clientthread, (clientAddress, ))
         
    
    except KeyboardInterrupt:
            #send message to all clients warning that server stopped
        for x in range(0,len(clients)):
            serverSocket.sendto(('Server exiting').encode(), clients[x])
        print('*** Server closed ***')
        serverSocket.close()
        sys.exit()