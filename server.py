#!/usr/bin/env python3

import socket, threading

HOST = '127.0.0.1'
PORT = 8555



def client_thread(sock, address):
    while True:
        msg = sock.recv(1024).decode()
        if not msg:
            break
        print(address, " ", msg)
    sock.close()

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Starting server at {}'.format(HOST))
    s.bind((HOST, PORT))

    s.listen(5)

    while True:
        conn, address = s.accept() #Accept connections from within while loop
        print("Connection from: {}".format(address))

        t1 = threading.Thread(target=client_thread, args=((conn, address)))
        t1.start() # Start a thread for the client.

    conn.close()


if __name__ == '__main__':
    server()