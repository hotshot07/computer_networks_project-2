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
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
print ('\n** CLIENT **\n')

try:
    #initial msg client sends to server so server can know address of client
    clientSocket.sendto(('Hello, I\'m a client').encode(),(serverName, serverPort))            
    
    #if error in server's address:
except socket.gaierror as msg:
    print ('Error code: ' + str(msg))
    clientSocket.close()
    sys.exit()
    
#client gets welcome message of server (proof that server is working)
welcome, serverAddress = clientSocket.recvfrom(2048)
print (str(welcome)[2:-1])
    
#client will do these actions repeteadly
while True:

    try:
            #client receives messages from server
        msg, serverAddress = clientSocket.recvfrom(2048)
        
            #in case server closes communication
        if msg == ('Server exiting').encode():
            #closes socket and process terminates
            clientSocket.close()
            sys.exit()
        
        if msg == ('Would you like to take a test? (Y/N)').encode():
            answer = input('Would you like to take a test? (Y/N): ')
            clientSocket.sendto(answer.encode(),(serverName, serverPort))
       
        else:
            print(str(msg)[2:-1])


    except KeyboardInterrupt:
        #if client exits (ctr+c) -> tell server
        clientSocket.sendto(('Client ' + str(clientSocket.getsockname())[12:17] + ' exiting').encode(),(serverName, serverPort))
        #closes socket and process terminates
        clientSocket.close()
        sys.exit()