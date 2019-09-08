#ON START CLIENT SHOULD BE SUPPLIED WITH SERVER IP AND CONTROL PORT NUMBER
from socket import *
import sys
import os

global control_port

class State:
    def __init__(self, clientSocket, serverName):
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = clientSocket
        self.server = serverName

if __name__ == '__main__':
    global control_port
    serverName = "127.0.0.1"
    #serverName = sys.argv[1]
    control_port = int(sys.argv[1])
    #control_port = int(sys.argv[2])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, control_port))
    state = State(clientSocket, serverName)

    while True:
        sentence = input('ftp> ')
        state.control.send(sentence.encode('ascii'))
        if(sentence == 'bye'):
            break
        text = state.control.recv(1024)
        print(text.decode('ascii'))

    state.control.close()
