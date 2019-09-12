#ON START CLIENT SHOULD BE SUPPLIED WITH SERVER IP AND CONTROL PORT NUMBER
from socket import *
import sys
import os
import json
os.system('color')

global control_port

class State:
    def __init__(self, client, server):
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = client
        self.server = server


def rls(state):
    state.control.send("ls".encode('ascii'))
    dir = state.control.recv(1024).decode('ascii')
    dirlist = json.loads(dir)
    for key, value in dirlist.items():
        if value == 'f':
            print(key, end='    ')
        else:
            CRED = '\033[91m'
            CEND = '\033[0m'
            print(CRED + key + CEND, end='    ')
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

def data_connection(state):
    data_port = int(state.control.recv(1024).decode('ascii'))
    state.data = socket(AF_INET, SOCK_STREAM)
    state.data.connect((state.server, data_port))

def get(state):
    state.control.send(state.command.encode('ascii'))
    data_connection(state)
    target = state.command[4:]
    try:
        f = open(target, 'wb+')
        data = state.data.recv(1024)
        while data:
            f.write(data)
            data = state.data.recv(1024)
        print('OK')
    except Exception as e:
        print(e)
    finally:
        state.data.close()


if __name__ == '__main__':
    global control_port
    server = "127.0.0.1"
    #server = sys.argv[1]
    control_port = int(sys.argv[1])
    #control_port = int(sys.argv[2])

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((server, control_port))
    state = State(client, server)
    server_user = state.control.recv(1024).decode('ascii')
    server_client_user = input('Name ({}:{}):'.format(server, server_user))
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
        elif(state.command[0:4] == "put "):
            put(state)
        else:
            print("Incorrect command!")


    state.control.close()
