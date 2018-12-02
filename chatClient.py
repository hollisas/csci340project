import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 80
server.connect((ip_address, port))

while(True):
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    
    for sockets in read_sockets:
        if sockets != server:
            message = sys.stdin.readline()
            server.sendall(message.encode('utf-8'))
            sys.stdout.write("[You]")
            sys.stdout.write(message)
            sys.stdout.flush()
        else:
            message = sockets.recv(2048).decode('utf_8')
            print(message)

server.close()