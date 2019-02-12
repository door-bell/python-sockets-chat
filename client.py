#!/usr/bin/env python3

import sys, socket, threading, time

HOST = '127.0.0.1'
PORT = 8555

def delete_last_lines(n=1):
    # Adapted from 
    # https://www.quora.com/How-can-I-delete-the-last-printed-line-in-Python-language
    for i in range(1, n):
        sys.stdout.write('\033[F') #back to previous line
        sys.stdout.write('\033[K') #clear line

def listen(sock, HOST, PORT):
    while True:
        data = sock.recv(1024).decode()
        sys.stdout.write('\033[K') #clear line
        print(data.join('\n'))

def client(sock, nick='Default'):
    t1 = threading.Thread(target=listen, args=(sock, HOST, PORT))
    t1.start()

    while True:
        message = input('{} > '.format(nick))  # take input
        sys.stdout.write('\033[K') #clear line
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