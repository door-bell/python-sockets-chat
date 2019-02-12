#!/usr/bin/env python3

import socket, threading

HOST = '127.0.0.1'
PORT = 8555

s = socket.socket()

s.connect((HOST, PORT))

def listen(HOST, PORT):
    while True:
        data = s.recv(1024).decode()
        print('Recieved: {}'.format(data))

def client():
    t1 = threading.Thread(target=listen, args=(HOST, PORT))
    t1.start()

    while True:
        message = input(" -> ")  # take input
        s.send(message.encode())

    s.close()  # close the connection


if __name__ == '__main__':
    client()