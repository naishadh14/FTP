#ON START SERVER SHOULD BE SUPPLIED WITH CONTROL PORT NUMBER
from socket import *
from threading import Thread
import sys
import os

global control_port

class State:
    def __init__(self, connectionSocket, addr):
        self.cwd = os.getcwd()
        self.folder = os.path.basename(self.cwd)
        self.control = connectionSocket
        self.addr = addr
        #ALSO DEFINE SELF.DATA

def ls(state):
    dirlist = os.listdir(state.cwd)
    for l in dirlist:
        print(l)
    state.control.send(state.command.encode('ascii'))

def connection(state):
    print("New connection to client {}".format(addr))
    while True:
        command = state.control.recv(1024).decode('ascii')
        #SWITCH BASED ON command
        if(command == "ls"):
            state.command = "ls"
            ls(state)

    state.control.close()

if __name__ == '__main__':
    global control_port
    control_port = int(sys.argv[1])
    control_socket = socket(AF_INET, SOCK_STREAM)
    control_socket.bind(('', control_port))
    control_socket.listen(10)

    while True:
        connectionSocket, addr = control_socket.accept()
        state = State(connectionSocket, addr)
        t = Thread(target=connection, args=(state,))
        t.start()

    control_socket.close()
