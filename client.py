#ON START CLIENT SHOULD BE SUPPLIED WITH SERVER IP AND CONTROL PORT NUMBER
from socket import *
import sys
import os
import json
os.system('color')

global control_port

class State:
    def __init__(self, clientSocket, dataSocket, serverName):
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = clientSocket
        self.data = dataSocket
        self.server = serverName


def rls(state):
    state.control.send("ls".encode('ascii'))
    dirs = state.data.recv(1024).decode('ascii')
    dirlist = json.loads(dirs)
    for l in dirlist:
        if '.' in l:
            print(l, end='    ')
        else:
            CRED = '\033[91m'
            CEND = '\033[0m'
            print(CRED + l + CEND, end='    ')
    print()

def lls(state):
    dirlist = os.listdir(state.cwd)
    for l in dirlist:
        print(l, end='    ')
    print()

def cd(state):
    pass

if __name__ == '__main__':
    global control_port
    serverName = "127.0.0.1"
    #serverName = sys.argv[1]
    control_port = int(sys.argv[1])
    #control_port = int(sys.argv[2])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, control_port))
    data_port = int(clientSocket.recv(1024).decode('ascii'))
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((serverName, data_port))
    state = State(clientSocket, dataSocket, serverName)
    print('The control port is {} and the data port is {}'.format(control_port, data_port))

    while True:
        command = input('ftp> ')
        #SWITCH BASED ON COMMAND
        if(command == "bye"):
            break
        elif(command == "ls"):
            rls(state)
        elif(command == "!ls"):
            lls(state)
        elif(command[0:3] == "cd "):
            state.command = command
            cd(state)
        else:
            print("Incorrect command!")


    state.control.close()
