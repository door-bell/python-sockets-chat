#!/usr/bin/env python3

import socket, threading

HOST = '127.0.0.1'
PORT = 8555

s = socket.socket()

def listen(HOST, PORT):
    while True:
        s.connect((HOST, PORT))
        data = s.recv(1024).decode()

        print('Recieved: {}'.format(data))

def client():
    t1 = threading.Thread(target=listen, args=(HOST, PORT))
    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        s.send(message.encode())  # send message
        data = s.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    s.close()  # close the connection


if __name__ == '__main__':
    client()