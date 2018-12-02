import socket
import select
import sys
import threading
import bot

ip_address = "127.0.0.1"
port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip_address, port)) 
server.listen(10)

client_list=[]

def client_thread(connection, address):

    connection.sendall(b"You are now online")
    
    while(True):
            try:     
                message = connection.recv(2048).decode('utf_8')    
                if message:
                    if message[:4] == "wiki":
                        botThread = threading.Thread(target=bot.main, args=(message[5:-1],))
                        botThread.start()
                        botThread.join()
                        thestring = bot.astring
                        message_to_send = "[" + address[0] + "] " + thestring
                        broadcast(message_to_send, connection)
                    else:
                        print("[" + address[0] + "] " + message)
                        message_to_send = "[" + address[0] + "] " + message
                        broadcast(message_to_send,connection)
                else:
                    remove(connection)

            # Exception handling not our code
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

def remove(connection):
    if connection in client_list:
        client_list.remove(connection)

def broadcast(message, connection):
    for clients in client_list:
        if clients != connection:
            try:
                clients.sendall(message.encode('utf-8'))
            except:
                clients.close()
                remove(clients)

while True:
    connection, address = server.accept()
    client_list.append(connection)
    print(address[0] + " connected")
    chat_client = threading.Thread(target=client_thread,args=(connection,address))
    chat_client.start()


connection.close()
server.close()