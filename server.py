#ON START SERVER SHOULD BE SUPPLIED WITH CONTROL PORT NUMBER
from socket import *
from threading import Thread
import sys
import os
import json

global control_port, thread_list
class State:
    def __init__(self, connectionSocket, addr, count):
        global control_port
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = connectionSocket
        self.control_addr = addr
        self.data_port = control_port + count
        self.data_socket = socket(AF_INET, SOCK_STREAM)
        self.data_socket.bind(('', self.data_port))
        #ALSO DEFINE SELF.DATA

def threads(control_socket):
    global thread_list
    while len(thread_list) == 0:
        continue
    if(len(thread_list) == 0):
        control_socket.close()
        sys.exit(0)

def ls(state):
    dirlist = os.listdir(state.cwd)
    state.data.send(json.dumps(dirlist).encode('ascii'))

def connection(state):
    print("New connection to client {}".format(addr))
    state.control.send(str(state.data_port).encode('ascii'))
    state.data_socket.listen(1)
    state.data, state.data_addr = state.data_socket.accept()
    while True:
        command = state.control.recv(1024).decode('ascii')
        #SWITCH BASED ON command
        if(command == "ls"):
            state.command = "ls"
            ls(state)

    state.data.close()
    state.control.close()

if __name__ == '__main__':
    global control_port, thread_list
    control_port = int(sys.argv[1])
    control_socket = socket(AF_INET, SOCK_STREAM)
    control_socket.bind(('', control_port))
    control_socket.listen(10)
    count = 1
    thread_list = []
    t = Thread(target=threads, args=(control_socket, ))
    t.start()

    while True:
        connectionSocket, addr = control_socket.accept()
        state = State(connectionSocket, addr, count)
        t = Thread(target=connection, args=(state,))
        t.start()
        count += 1
        thread_list.append(t)

    control_socket.close()
