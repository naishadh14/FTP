#ON START SERVER SHOULD BE SUPPLIED WITH CONTROL PORT NUMBER
from socket import *
from threading import Thread
import sys
import os
import json
import getpass

global control_port
class State:
    '''
    This class contains the following variables
    Hidden: self.command, self.dirlist, self.data, self.data_addr
    '''
    def __init__(self, connectionSocket, addr, count):
        global control_port
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = connectionSocket
        self.control_addr = addr
        self.data_port = control_port + count
        self.data_socket = socket(AF_INET, SOCK_STREAM)
        self.data_socket.bind(('', self.data_port))

def ls(state):
    state.dirlist = os.listdir(state.cwd)
    state.data.send(json.dumps(state.dirlist).encode('ascii'))

def cd(state):
    target = state.command[3:]
    try:
        os.chdir(target)
        state.cwd = os.getcwd()
        state.folder = target
        state.data.send('OK'.encode('ascii'))
    except Exception as e:
        state.data.send(str(e).encode('ascii'))

def pwd(state):
    state.data.send(state.cwd.encode('ascii'))

def get(state):
    target = state.command[4:]
    if os.path.isfile(target):
        try:
            f = open(target, 'rb')
            l = f.read(1024)
            while(l):
                state.data.send(l)
                l = f.read(1024)
        except Exception as e:
            state.data.send(e.encode('ascii'))


def connection(state):
    print("New connection to client {}".format(addr))
    state.control.send(str(state.data_port).encode('ascii'))
    state.data_socket.listen(1)
    state.data, state.data_addr = state.data_socket.accept()
    state.user_name = getpass.getuser()
    print('{} Asking for connection'.format(state.user_name))
    state.control.send(str(state.user_name).encode('ascii'))
    
    if(state.user_name == state.control.recv(1024).decode('ascii')):

        while True:
            state.command = state.control.recv(1024).decode('ascii')
            #SWITCH BASED ON command
            if(state.command == "ls"):
                ls(state)
            elif(state.command[0:3] == "cd "):
                cd(state)
            elif(state.command == "pwd"):
                pwd(state)
            elif(state.command[0:4] == "get "):
                get(state)

    state.data.close()
    state.control.close()

if __name__ == '__main__':
    global control_port
    control_port = int(sys.argv[1])
    control_socket = socket(AF_INET, SOCK_STREAM)
    control_socket.bind(('', control_port))
    control_socket.listen(10)
    count = 1
    print('Waiting for incoming connections')

    while True:
        connectionSocket, addr = control_socket.accept()
        state = State(connectionSocket, addr, count)
        t = Thread(target=connection, args=(state,))
        t.start()
        count += 1

    control_socket.close()
