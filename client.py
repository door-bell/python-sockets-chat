#!/usr/bin/env python3
'''
Notes on speicial characters used in stdout:
        \033[F # Back to previous line
        \033[K # Clear line
        \r # Carriage return: brings cursor to beginning of the line.
'''
import sys, socket, threading, time

HOST = '127.0.0.1'
PORT = 8555

# Printing to stdout is NOT thread safe
stdout_lock = threading.Lock()

def listen(sock, HOST, PORT):
    while True:
        data = sock.recv(1024).decode()
        stdout_lock.acquire()
        sys.stdout.write('\r\033[K' + data)
        sys.stdout.flush()
        sys.stdout.write('\n')
        stdout_lock.release()

def client(sock, nick='Default'):
    t1 = threading.Thread(target=listen, args=(sock, HOST, PORT), daemon=True)
    t1.start()

    while True:
        message = input('{} > '.format(nick))  # take input
        stdout_lock.acquire()
        sys.stdout.write('\033[F\033[K')
        stdout_lock.release()
        sock.send('{}: {}'.format(nick, message).encode())
        if message.endswith('later'):
            break

    print('Quitting...')
    sock.close()  # close the connection
    quit(0)

if __name__ == '__main__':
    # Uncomment to allow custom host:port from user
    # HOST = str(input('Enter host: '))
    # PORT = int(input('Enter port:'))
    nick = str(input('Enter nickname: '))

    s = socket.socket()
    s.connect((HOST, PORT))

    client(sock=s, nick=nick)