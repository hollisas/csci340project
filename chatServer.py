import socket
import select
from _thread import *
import sys
import threading
import bot

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
server.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr):
    conn.sendall(b"Welcome to this chatroom!")
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048).decode('utf_8')    
                if message:
                    if message[:4] == "wiki":
                        botThread = threading.Thread(target=bot.main, args=(message[5:-1],))
                        botThread.start()
                        botThread.join()
                        thestring = bot.astring
                        broadcast(thestring, conn)
                    else:
                        print("[" + addr[0] + "] " + message)
                        message_to_send = "[" + addr[0] + "] " + message
                        broadcast(message_to_send,conn)

                    print("past that stuff")
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.sendall(message.encode('utf-8'))
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects

conn.close()
server.close()