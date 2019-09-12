#ON START CLIENT SHOULD BE SUPPLIED WITH SERVER IP AND CONTROL PORT NUMBER
from socket import *
import sys
import os
import json
os.system('color')

global control_port

class State:
    def __init__(self, clientSocket, dataSocket, serverName, data_port):
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = clientSocket
        self.data = dataSocket
        self.server = serverName
        self.data_port = data_port


def rls(state):
    state.control.send("ls".encode('ascii'))
    dirs = state.control.recv(1024).decode('ascii')
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
    print(state.control.recv(1024).decode('ascii'))

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
    print(state.control.recv(1024).decode('ascii'))

def lpwd(state):
    print(state.cwd)

def get(state):
    state.control.send(state.command.encode('ascii'))
    target = state.command[4:]
    try:
        state.data.connect((state.server, state.data_port))
        f = open(target, 'wb+')
        data = state.data.recv(1024)
        while data:
            f.write(data)
            data = state.data.recv(1024)
        print('OK')
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
    state = State(clientSocket, dataSocket, serverName, data_port)
    print('The control port is {} and the data port is {}'.format(control_port, data_port))
    server_user = state.control.recv(1024).decode('ascii')
    server_client_user = input('Name ({}:{}):'.format(serverName, server_user))
    state.control.send(server_client_user.encode('ascii'))

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
