import sys
import socket
import time
import threading
from threading import Thread
from SocketServer import ThreadingMixIn

JOINING_GAME = 1
CM_SUBSCRIBE = 'Name of the Player : '
SM_NEW_GAME = ''
GAME_IN_PROGRESS = 0
RINGED = 0
Ring_recieved=0

class ServerThread(Thread):

    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        global JOINING_GAME
        global SM_NEW_GAME
        global GAME_IN_PROGRESS
        global CM_SUBSCRIBE
        global Ring_recieved
        while True:
            starttime = time.time()
            if GAME_IN_PROGRESS == 1:
                self.category()

    def category(self):
        while True:
            category = self.socket.recv(BUFFER_SIZE)
            catmsg = "Choose a category: 1. Protocols  2. Commands  3. Security "
            check_ring="RING! RING! RING! (Enter any key)"
            check_ans="What is your answer? "
            end_msg="End of round! (Enter any key to continue) "

            if (category == catmsg) == True:
                cat = raw_input(category)
                self.socket.send(cat)
            elif category==check_ring:
                ring=raw_input(check_ring)
                self.socket.send(ring)
            elif category==check_ans:
                answer=raw_input(check_ans)
                self.socket.send(answer)
            elif category == end_msg:
                k=raw_input(end_msg)
                self.socket.send(k)
            else :
                print category

class ServerThreadread(Thread):

    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        global RINGED
        global GAME_IN_PROGRESS
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((TCP_IP, TCP_PORT2))
        while True:
            if log == 0:
                chat=s2.recv(BUFFER_SIZE)
                print chat
                if (str(chat) == "Game Begins!") == True:
                    GAME_IN_PROGRESS = 1
            if log == 1:
                s2.close()
                sys.exit()

TCP_IP = '127.0.0.1'
TCP_PORT = 9002
TCP_PORT2 = 9003
BUFFER_SIZE = 1024
threads = []
global log
log = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
TIME_OUT = s.recv(BUFFER_SIZE)
count = [1, 2, 3]
status = 0
while status == 0:
    username = raw_input(CM_SUBSCRIBE)
    s.send(username)
    ack1 = s.recv(BUFFER_SIZE)
    print ack1
    status = 1
    JOINING_GAME = 0

if ( status == 1 ):
    try:
        newthread = ServerThread(s)
        newthread.daemon = True
        newthread2 = ServerThreadread(s)
        newthread2.daemon = True
        newthread.start()
        newthread2.start()
        threads.append(newthread)
        threads.append(newthread2)
        while True:
            for t in threads:
                t.join(400)
                if not t.isAlive():
                    break
            break

    except KeyboardInterrupt:
        command = "logout"
        s.send(command)
        sys.exit()
