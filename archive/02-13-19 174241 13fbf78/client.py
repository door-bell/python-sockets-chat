#!/usr/bin/env python3

# \033[F # Back to previous line
# \033[K # Clear line

import sys, socket, threading, time

HOST = '127.0.0.1'
PORT = 8555


def listen(sock, HOST, PORT):
    while True:
        data = sock.recv(1024).decode()
        sys.stdout.write('\r\033[K' + data)
        sys.stdout.flush()
        sys.stdout.write('\n')

def client(sock, nick='Default'):
    t1 = threading.Thread(target=listen, args=(sock, HOST, PORT))
    t1.start()

    while True:
        message = input('{} > '.format(nick))  # take input
        sys.stdout.write('\033[F\033[K')
        sock.send('{}: {}'.format(nick, message).encode())

    sock.close()  # close the connection


if __name__ == '__main__':
    # Uncomment to allow custom host:port from user
    # HOST = str(input('Enter host: '))
    # PORT = int(input('Enter port:'))
    nick = str(input('Enter nickname: '))

    s = socket.socket()
    s.connect((HOST, PORT))

    client(sock=s, nick=nick)