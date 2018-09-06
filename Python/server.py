import socket
import sys
import collections
import time
import Queue
import threading
import random

from threading import Thread, Event,Semaphore
from SocketServer import ThreadingMixIn

event=Event()
COLLECT_SUBSCRIPTIONS = 1
CM_SUBSCRIBE =''
SM_NEW_GAME = 'Game Begins!'
GAME_IN_PROGRESS = 0
START_ROUND = 0
RINGING = 0
trial = 0
var = 0
var1 = 0
var2 = 0
var3 = 0
var4 = 0
lock = threading.Lock()
global command
command = ""
threads =[]
masterName = ''
key=0

class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count = self.count + 1
        self.mutex.release()
        if self.count == self.n: self.barrier.release()
        self.barrier.acquire()
        self.barrier.release()
blist=[Barrier(3),Barrier(3),Barrier(3),Barrier(3),Barrier(3),Barrier(3),Barrier(3)]
cat_count = 0
cat =''

game_queues = {}
categories = ['protocols ','commands ','security']
q_set={1: [('Most commonly used routable protocol suite for internetworking', 'tcp'),
('Most widely used protocol for internetworking', 'ip')],
2: [('Resolving the IP to the MAC address using _________', 'arp'),
('This protocol is used to send communication error messages', 'icmp')],
3: [('The "ping of death" or an attack known as a Smurf Attack', 'icmp'),
('A collection of computers infected with software robots that can be controlled remotely', 'botnet')]}

class ClientThread(Thread):
    def __init__(self,socket,ip,port):
        Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = port

    def run(self):
        global count
        global CM_SUBSCRIBE
        global key
        global var
        global round
        global var1

        round=0
        user_info = 0
        i = 0
        while True:
            if user_info not in cur_users:
                self.socket.send(str(TIME_OUT))
                CM_SUBSCRIBE = self.socket.recv(2048)
                welcome_msg = "Welcome to the Jeopardy Game!"
                self.socket.send(welcome_msg)
                lock.acquire()
                cur_users.append(CM_SUBSCRIBE)
                lock.release()
                io = self.socket.fileno()
                io_user = CM_SUBSCRIBE + " " + str(io)
                lock.acquire()
                user_io_map.append(io_user)
                lock.release()
                self.getData(user_info)
                while(round < 6):
                    if(round>0):
                        if(var1==0):
                            var1+=1
                            self.selectMaster()
                    if var<=1:
                        var+=1
                        event.wait()
                        event.clear()
                    ring_alert = "RING! RING! RING! (Enter any key)"
                    self.socket.send(ring_alert)
                    response=self.socket.recv(1024)
                    if key==0:
                        key+=1
                        for x in user_io_map:
                            y = x.partition(" ")
                            if y[2] == str(self.socket.fileno()):
                                ring_owner = str(y[0])
                        ring_msg = "\n"+str(ring_owner) + " rang! "
                        self.broadcast(ring_msg)
                        ans_msg="What is your answer? "
                        self.socket.send(ans_msg)
                        answer=self.socket.recv(1024)
                        if(answer.lower() == question[1]):
                            r_msg="The Answer is Correct!"
                            self.broadcast(r_msg)
                            var1=0
                            end="End of round! (Enter any key to continue) "
                            end1="Next round will start momentarily, please don't press any key!"
                            for x in user_io_map:
                                y = x.partition(" ")
                                if y[2] not in str(self.socket.fileno()) :
                                    gmaster_io = int(y[2])
                                    lock.acquire()
                                    game_queues[gmaster_io].put(end)
                                    lock.release()
                                if y[2] == str(self.socket.fileno()):
                                    gmaster_io = int(y[2])
                                    lock.acquire()
                                    game_queues[gmaster_io].put(end1)
                                    lock.release()
                            round+=1
                        else:
                            w_msg="Incorrect Answer!"
                            self.broadcast(w_msg)
                            var1=0
                            end="End of round! (Enter any key to continue) "
                            end1="Next round will start momentarily, please don't press any key!"
                            for x in user_io_map:
                                y = x.partition(" ")
                                if y[2] not in str(self.socket.fileno()) :
                                    gmaster_io = int(y[2])
                                    lock.acquire()
                                    game_queues[gmaster_io].put(end)
                                    lock.release()
                                if y[2] == str(self.socket.fileno()):
                                    gmaster_io = int(y[2])
                                    lock.acquire()
                                    game_queues[gmaster_io].put(end1)
                                    lock.release()
                            round+=1
                    elif key == 1:
                          msgnew = "Next Round"
                          self.broadcast(msgnew)
                    blist[round].wait()
                    var=0
                    key=0

    def getData(self,user_info):
        global COLLECT_SUBSCRIPTIONS
        global GAME_IN_PROGRESS

        if max_users > 0 | COLLECT_SUBSCRIPTIONS == 1:
            message = "Waiting for users to join"
        elif max_users == 0:
            print ("All players have joined. ")
            p_input = "Players : \n"
            for x in user_io_map:
                y = x.partition(" ")
                p_input = p_input + str(y[0]) +"\n"
            self.broadcast(SM_NEW_GAME)
            self.broadcast(p_input)
            COLLECT_SUBSCRIPTIONS = 0
            GAME_IN_PROGRESS = 1
            self.selectMaster()
        return 1

    def selectMaster(self):
        global START_ROUND
        global masterName
        global gmaster_io
        gmaster_io = ''
        count = random.randint(0,(len(cur_users)-1))
        i = 0
        messageMaster = ''

        for x in user_io_map:
            if i == count:
                y = x.partition(" ")
                masterName = y[0]
                gmaster_io = int(y[2])
                lock.acquire()
                game_queues[gmaster_io].put("You are randomly chosen as the Game Master\n")
                lock.release()
                messageMaster = masterName + " is the Game Master for this round"
                print messageMaster
                self.broadcast(messageMaster)
                time.sleep(1)
                self.selectCat(gmaster_io)
            i = i + 1
        if START_ROUND == 1:
            self.startRound()
        return 1

    def selectCat(self, mastervalue):
        global categories
        global cat_count
        global cat

        cat_msg = "Choose a category: 1. Protocols  2. Commands  3. Security "
        cat_msg_sel = ''
        for players in curuser_conn:
            if players.fileno() == mastervalue:
                while (True):
                    players.send(cat_msg)
                    cat = players.recv(BUFFER_SIZE)
                    break
        cat_msg_sel = "The selected category is "+ str(categories[int(cat)-1])
        self.broadcast("Round Begins!")
        self.broadcast(cat_msg_sel)
        self.questions(cat)
        return 1

    def questions(self, catNumber):
        global var2
        global var3
        global var4
        global var
        global question
        global cat_count
        global gmaster_io
        catMessage = str(categories[int(catNumber) - 1]) + "All Questions Answered in this category"
        if (catNumber == "1"):
            if (var2 == 0):
                question=q_set[1][0]
                var2+=1
                self.broadcast(question[0])
            elif( var2==1):
                question=q_set[1][1]
                var2+=1
                self.broadcast(question[0])
            else :
                cat_count = 1
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.selectCat(gmaster_io)
                return


        elif(catNumber=="2"):
            if(var3==0):
                question=q_set[2][0]
                var3+=1
                self.broadcast(question[0])
            elif(var3==1):
                question=q_set[2][1]
                var3+=1
                self.broadcast(question[0])
            else :
                cat_count = 2
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.selectCat(gmaster_io)
                return


        elif(catNumber=="3"):
            if(var4==0):
                question=q_set[3][0]
                var4+=1
                self.broadcast(question[0])
            elif(var4==1):
                question=q_set[3][1]
                var4+=1
                self.broadcast(question[0])
            else:
                cat_count = 3
                self.broadcast(catMessage)
                time.sleep(0.5)
                self.selectCat(gmaster_io)
                return
        time.sleep(1)
        event.set()
        return 1

    def broadcast(self, message):
        lock.acquire()
        for clients in game_queues.values():
                clients.put(message)
                time.sleep(0.75)
        lock.release()

class ClientThreadread(Thread):
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock

    def run(self):
         global trial
         global RINGING
         i = 0
         tcpsock2.listen(1)
         (conn2, addr) = tcpsock2.accept()
         while True:
             for p in user_io_map:
                 if str(self.sock.fileno()) in p:
                    connectionpresent = 1
                 else:
                    connectionpresent = 0
             try:
                 chat = game_queues[self.sock.fileno()].get(False)
                 conn2.send(chat)
             except Queue.Empty:
                 chat = "none"
                 time.sleep(2)
             except KeyError, e:
                 pass

TCP_IP = '0.0.0.0'
TCP_PORT = 9002
TCP_PORT2 = 9003
BUFFER_SIZE = 1024
TIME_OUT = 1600.0
BLOCK_TIME = 40.0

max_users=3
curr_users=0
cur_users = []
curuser_conn = []
userlog = {}
user_io_map = []

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(('', TCP_PORT))

tcpsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock2.bind(('', TCP_PORT2))

while True:

    if max_users != 0:
        tcpsock.listen(4)
        print "Waiting for users to join... "
        (conn, (ip,port)) = tcpsock.accept()
        max_users = max_users - 1
        if max_users == 0:
            COLLECT_SUBSCRIPTIONS = 0
        q = Queue.Queue()
        lock.acquire()
        curuser_conn.append(conn)
        userlog[conn.fileno()] = conn
        game_queues[conn.fileno()] = q
        lock.release()
        newthread = ClientThread(conn,ip,port)
        newthread.daemon = True
        newthread.start()
        newthread2 = ClientThreadread(conn)
        newthread2.daemon = True
        newthread2.start()
        threads.append(newthread)
        threads.append(newthread2)

for t in threads:
    t.join()
