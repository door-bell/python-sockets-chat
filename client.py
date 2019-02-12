#!/usr/bin/env python3

import socket, threading, time

HOST = '127.0.0.1'
PORT = 8555

def listen(sock, HOST, PORT):
    while True:
        data = sock.recv(1024).decode()
        print(data)

def client(sock, nick='Default'):
    t1 = threading.Thread(target=listen, args=(sock, HOST, PORT))
    t1.start()

    while True:
        message = input('{} -> '.format(nick))  # take input
        sock.send('{}: {}'.format(nick, message).encode())
        time.sleep(0.5)

    sock.close()  # close the connection


if __name__ == '__main__':
    # Uncomment to allow custom host:port from user
    # HOST = str(input('Enter host: '))
    # PORT = int(input('Enter port:'))
    nick = str(input('Enter nickname: '))

    s = socket.socket()
    s.connect((HOST, PORT))

    client(sock=s, nick=nick)