#!/usr/bin/env python3

import socket, threading, re
from queue import Queue

HOST = '127.0.0.1'
PORT = 8555

g_clientDict = dict()
g_msgQueue = Queue()

lock_clientDict = threading.Lock()
lock_msgQueue = threading.Lock()

def verifyNick(nick):
    return nick not in g_clientDict

def enqueueMessage(msg):
    lock_msgQueue.acquire()
    g_msgQueue.put(msg.encode())
    lock_msgQueue.release()

def handleCommand(cmd, nick, sock):
    command = cmd[1:].split(' ')
    print('Received command {} from {}'.format(command, nick))

    # Commands
    if command[0] == 'hello':
        enqueueMessage('{} greets everyone.'.format(nick))
    elif command[0] == 'w':
        lock_clientDict.acquire()
        dest = g_clientDict[command[1]]
        lock_clientDict.release()
        join = ' '.join(command[2:])
        msg = 'Whisper to {}: {}'.format(command[1], join).encode()
        sock.send(msg)
        msg = 'Whisper from {}: {}'.format(nick, join).encode()
        dest.send(msg)

def client_thread(sock, address, nick):
    while True:
        msg = sock.recv(1024).decode()
        if len(msg) is 0: # Detect abrupt disconnect
            break
        print(address, ' ', nick, ':', msg)

        # The / of a command should be 2 characters right of :
        if msg[0] is '/':
            handleCommand(msg, nick, sock)
            continue

        enqueueMessage('{}: {}'.format(nick, msg))

    sock.send('\nGoodbye!'.encode())
    sock.close()
    lock_clientDict.acquire()
    g_clientDict.pop(nick)
    lock_clientDict.release()
    print('Removed {} from clientDict'.format(nick))
    return 0

def broadcast_thread():
    # Send all enqueued messages to each client
    while True:
        while not g_msgQueue.empty():
            lock_msgQueue.acquire()
            msg = g_msgQueue.get()
            lock_msgQueue.release()

            lock_clientDict.acquire()
            for sock in g_clientDict.values():
                sock.send(msg)
            lock_clientDict.release()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Starting server at {}'.format(HOST))
    s.bind((HOST, PORT))

    s.listen(5)

    # Open thread to broadcast to connected clients
    broadcastThread = threading.Thread(target=broadcast_thread, daemon=True)
    broadcastThread.start()

    # Accept connections and open a thread for each one
    while True:
        #Accept connections from within while loop
        nick = None
        conn, address = s.accept() 
        conn.settimeout(3)
        try:
            nick = conn.recv(1024).decode()
            if not verifyNick(nick):
                raise Exception('Invalid nickname: {}'.format(nick))
            else:
                print("New connection: {}".format(nick))
        except Exception as ex:
            print(ex)
            conn.close()
            continue

        conn.settimeout(None)
        conn.send('OK'.encode()) # Send OK signal
        lock_clientDict.acquire()
        g_clientDict[nick] = conn
        lock_clientDict.release()
        # Start a thread for the client.
        t1 = threading.Thread(target=client_thread, args=(conn, address, nick), daemon=True)
        t1.start()


if __name__ == '__main__':
    server()