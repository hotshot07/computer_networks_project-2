#for handling socket errors:
import socket
#if client leaves -> sys.exit() for properly terminating process:
import sys

#destination host's IP Adress + destination socket's port number
serverName = 'localhost'

#server port number arbitrarily chosen 
serverPort = 2112
  
#CREATING CLIENT'S SOCKET
    #AF_INET indicates that the underlying network is using IPv4
    #SOCK_DGRAM indicates this is a UDP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
print ('\n** CLIENT **')

remote_ip = socket.gethostbyname( serverName )

try:
    #Connect to remote server
    clientSocket.connect((remote_ip , serverPort))
    #if server not connected
except socket.error as msg:
    print ('Server not connected\nError code: ' + str(msg) + "!")
    clientSocket.close()
    sys.exit()

#initial msg client sends to server so server can know address of client
clientSocket.send(('Hello, I\'m a client').encode())            

    
#client gets welcome message of server (proof that server is working)
welcome = clientSocket.recv(2048)
print (str(welcome)[2:-1])
    
#client will do these actions repeteadly
while True:

    try:
            #client receives messages from server
        msg = clientSocket.recv(2048)
        
            #in case server closes communication
        if msg == ('Server exiting').encode():
            #closes socket and process terminates
            print('Server disconnected')
            clientSocket.close()
            sys.exit()
        
        if msg == ('Would you like to take a test? (Y/N)').encode():
            answer = input('Would you like to take a test? (Y/N): ')
            clientSocket.send(answer.encode())
       
        else:
            print(str(msg)[2:-1])


    except KeyboardInterrupt:
        #if client exits (ctr+c) -> tell server
        clientSocket.send(('Client exiting').encode())
        #closes socket and process terminates
        clientSocket.close()
        sys.exit()