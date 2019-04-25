#!/usr/bin/python
# coding: utf-8

from socket import *

def main():
    SERVER_NAME = 'localhost'
    SERVER_PORT = 12000

    client_socket = socket(AF_INET, SOCK_DGRAM)
    try:

        while True:

            message = "tere1"
            client_socket.sendto(message, (SERVER_NAME, SERVER_PORT))

            modifiedMessage, serverAddress = client_socket.recvfrom(2048)
            print 'Mensagem recebida:', modifiedMessage
    except KeyboardInterrupt:
        client_socket.close()

if __name__ == '__main__':
    main()
