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
        if os.path.isfile(l):
            print(l, end='    ')
        else:
            CRED = '\033[91m'
            CEND = '\033[0m'
            print(CRED + l + CEND, end='    ')
    print()

def lls(state):
    dirlist = os.listdir(state.cwd)
    for l in dirlist:
        if os.path.isfile(l):
            print(l, end='    ')
        else:
            CRED = '\033[91m'
            CEND = '\033[0m'
            print(CRED + l + CEND, end='    ')
    print()

def rcd(state):
    state.control.send(state.command.encode('ascii'))
    print(state.data.recv(1024).decode('ascii'))

def lcd(state):
    target = state.command[4:]
    try:
        os.chdir(target)
        state.cwd = os.getcwd()
        state.folder = target
        print('OK')
    except Exception as e:
        print(e)

def rpwd(state):
    state.control.send(state.command.encode('ascii'))
    print(state.data.recv(1024).decode('ascii'))

def lpwd(state):
    print(state.cwd)

def get(state):
    state.control.send(state.command.encode('ascii'))
    target = state.command[4:]
    try:
        f = open(target, 'wb')
        while True:
            data = state.data.recv(1024)
            if not data:
                break
            f.write(data)
    except Exception as e:
        print(e)


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
        state.command = input('ftp> ')
        #SWITCH BASED ON COMMAND
        if(state.command == "bye"):
            break
        elif(state.command == "ls"):
            rls(state)
        elif(state.command == "!ls"):
            lls(state)
        elif(state.command[0:3] == "cd "):
            rcd(state)
        elif(state.command[0:4] == "!cd "):
            lcd(state)
        elif(state.command == "pwd"):
            rpwd(state)
        elif(state.command == "!pwd"):
            lpwd(state)
        elif(state.command[0:4] == "get "):
            get(state)
        else:
            print("Incorrect command!")


    state.control.close()
