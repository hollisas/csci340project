import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 802
try:
    server.connect((ip_address, port))
except:
    print("Server is not online")
    exit()

while(True):
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for sockets in read_sockets:
        if sockets != server:
            message = sys.stdin.readline()
            if message[:5] != "!wiki":
                message = message[:-1]
            server.sendall(message.encode('utf-8'))
        else:
            message = sockets.recv(2048).decode('utf_8')
            print(message)

server.close()