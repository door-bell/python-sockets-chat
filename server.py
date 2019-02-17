#!/usr/bin/env python3

import socket, threading, re
from queue import Queue

HOST = '127.0.0.1'
PORT = 8555

g_clientList = list()
g_msgQueue = Queue()
lock_clientList = threading.Lock()
lock_msgQueue = threading.Lock()

def enqueueMessage(msg):
    lock_msgQueue.acquire()
    g_msgQueue.put(msg.encode())
    lock_msgQueue.release()

def handleCommand(cmd):
    ls = re.match(r'(.+): /(.+)', cmd).groups()
    print('Received command {} from {}'.format(ls[1], ls[0]))

    # Commands
    if ls[1] == 'hello':
        enqueueMessage('{} has connected!'.format(ls[0]))

def client_thread(sock, address):
    while True:
        msg = sock.recv(1024).decode()
        if len(msg) is 0: # Detect abrupt disconnect
            break
        print(address, ' ', msg)

        # The / of a command should be 2 characters right of :
        if msg[msg.index(':') + 2] is '/':
            handleCommand(msg)
            continue

        enqueueMessage(msg)

    sock.send('\nGoodbye!'.encode())
    sock.close()
    lock_clientList.acquire()
    g_clientList.remove(sock)
    print('Removed {} from clientList'.format(sock))
    lock_clientList.release()
    return 0

def broadcast_thread():
    # Send all enqueued messages to each client
    while True:
        while not g_msgQueue.empty():
            lock_msgQueue.acquire()
            msg = g_msgQueue.get()
            lock_msgQueue.release()

            lock_clientList.acquire()
            for client in g_clientList:
                client.send(msg)
            lock_clientList.release()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Starting server at {}'.format(HOST))
    s.bind((HOST, PORT))

    s.listen(5)

    # Open thread to broadcast to connected clients
    broadcastThread = threading.Thread(target=broadcast_thread)
    broadcastThread.start()


    # Accept connections and open a thread for each one
    while True:
        #Accept connections from within while loop
        conn, address = s.accept() 
        print('Connection from: {}'.format(address))
        lock_clientList.acquire()
        g_clientList.append(conn)
        lock_clientList.release()
        # Start a thread for the client.
        t1 = threading.Thread(target=client_thread, args=((conn, address)))
        t1.start()


if __name__ == '__main__':
    server()