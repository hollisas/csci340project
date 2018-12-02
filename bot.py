import socket
import select
#from _thread import *
import os
import requests
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "127.0.0.1"
Port = 80

#global message1 = ""

def connect():
    print("Running connection script\n")
    #os.system("python3 chatClient.py 127.0.0.1 80")

    # if len(sys.argv) != 3:
    #     print("Correct usage: script, IP address, port number")
    #     exit()
    server.connect((IP_address, Port))
    print("Joined chat room.\n")
    #while(True):
    #    print("Chaos everywhere...")
    while True:
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048).decode('utf_8')
                print(message)
            else:
                message = sys.stdin.readline()
                server.sendall(message.encode('utf-8'))
                sys.stdout.write("[You]")
                sys.stdout.write(message)
                sys.stdout.flush()
# 	# 		    #break

#     #server.close()

def get_request(topic):

    URL = "https://en.wikipedia.org/wiki/" + topic
    response = requests.get(url = URL)

    response2 = list(response.iter_lines())
    parse(response2, topic)

def parse(text_response, topic):

    lines = []
    for item in text_response:
        lines.append(item.decode('utf-8'))
    line = ""

    found = False
    for index, item in enumerate(lines):
        item_lower = item.lower()
        # find ambigous cases
        if "refer to" in item or "refers to" in item:
            print("Term too ambigous, please try again")
            print(index)
            exit(0)

        # find first <p> tag containing search term
        if "<p>" in item_lower[0:5] and topic in item_lower:
            found = True
            line = lines[index]
            break

    if found == False:
        print("Term too ambigous, please try again")
        exit(0)

    # make line into iterable list
    line_array = list(line)

    astring = "" 
    index = 0
    
    while line_array[index] != ".":
        # skip all text between angle brackets
        if line_array[index] == "<":
            while line_array[index] != ">":
                index += 1
            index += 1
        # skip all text between brackets
        elif line_array[index] == "[":
            while line_array[index] != "]":
                index += 1
            index += 1
        # skip all text between parentheses
        elif line_array[index] == "(":
            astring = astring[:-1]
            paren = 1 # start keeping track of paren pairs
            index += 1 # move past current paren
            while paren != 0:
                if line_array[index] == "(":
                    paren += 1
                elif line_array[index] == ")":
                    paren -= 1
                index += 1
        # add text to string
        else:
            astring += line_array[index]
            index += 1

    astring += "."

    message1 = astring

    print(astring)


def main():
    connect()
    topic = input("Enter a topic: ")
    get_request(topic)
    #connect()
    #get_request(sys.argv[1])

#if __name__ == main():
#    pass

main()
