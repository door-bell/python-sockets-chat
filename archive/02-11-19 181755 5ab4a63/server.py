#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 8555

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Starting server at {}'.format(HOST))
    s.bind((HOST, PORT))

    s.listen(5)

    conn, address = s.accept()
    print("Connection from: {}".format(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: {}".format(str(data)))
        data = input (' -> ')
        conn.send(data.encode())
    
    conn.close()


if __name__ == '__main__':
    server()