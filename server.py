#!/usr/bin/env python3

import socket, threading, re
from queue import Queue

HOST = '127.0.0.1'
PORT = 8555

clientList = list()
msgQueue = Queue()
clientList_lock = threading.Lock()
msgQueue_lock = threading.Lock()

def handleCommand(cmd):
    ls = re.match(r'(.+): /(.+)', cmd)
    print('Received command {} from {}'.format(ls[1], ls[0]))

    # Commands
    if ls[1] is 'hello':
        msgQueue_lock.acquire()
        msgQueue.put('{} has Connected!'.format(ls[0]))
        msgQueue_lock.release()

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

        msgQueue_lock.acquire()
        msgQueue.put(msg.encode())
        msgQueue_lock.release()

    sock.send('\nGoodbye!'.encode())
    sock.close()
    clientList_lock.acquire()
    clientList.remove(sock)
    print('Removed {} from clientList'.format(sock))
    clientList_lock.release()
    return 0

def broadcast_thread():
    # Send all enqueued messages to each client
    while True:
        while not msgQueue.empty():
            msgQueue_lock.acquire()
            msg = msgQueue.get()
            msgQueue_lock.release()

            clientList_lock.acquire()
            for client in clientList:
                client.send(msg)
            clientList_lock.release()

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
        clientList_lock.acquire()
        clientList.append(conn)
        clientList_lock.release()
        # Start a thread for the client.
        t1 = threading.Thread(target=client_thread, args=((conn, address)))
        t1.start()


if __name__ == '__main__':
    server()