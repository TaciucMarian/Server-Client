import random
import socket
import time
from _thread import *

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 50110  # Port to listen on (non-privileged ports are > 1023)
ThreadCount = 0
boolean=False



def threaded_client(connection):
    global boolean
    while True:
        data = connection.recv(1024)
        if not data:
            break
        data=data.decode('utf-8')
        if boolean:
            if data=='cmd1':
                n=random.randint(10,100)
                reply='Number Generated: ' + str(n)
            elif data=='cmd2':
                with open('text.txt', encoding='utf8') as var:
                    line=var.readline()
                    reply=line.split()[0]

        else:
            reply='Serverul nu a primit keepalive in ultimele 5 sec'


        connection.sendall(str.encode(reply))
    connection.close()

def thread_client_keepalive(connection):
    connection.settimeout(5.0)
    global boolean
    temp = time.time()  # iau timpul curent
    reply=''
    try:
        contor = None
        while True:
            if contor == None:
                contor = time.time()
            data = connection.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            if data == 'KeepAlive':
                if temp - contor > 5:
                    boolean = False
                else:
                    boolean = True
                contor = temp
                reply = 'Server Says: ' + data
            connection.sendall(str.encode(reply))
        connection.close()
    except Exception:
        boolean=False




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('Waitiing for a Connection..')
    s.listen(2)
    while True:
        conn, addr = s.accept()
        if ThreadCount==0:
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(thread_client_keepalive, (conn,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))
        else:
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(threaded_client, (conn,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

    s.close()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received', repr(data))
            conn.sendall(data)
