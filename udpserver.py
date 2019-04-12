#!/usr/bin/python
# coding: utf-8

import time;
from socket import *
from playsound import playsound
#playsound('audio.mp3')

class Transmissor(object):
    """docstring for Transmissor"""
    def __init__(self,port):
        super(Transmissor, self).__init__()
        #self.arg = arg
        self.server_socket = socket(AF_INET, SOCK_DGRAM);
        self.SERVER_PORT = port
        self.server_socket.bind(('', self.SERVER_PORT))

    def enviaArquivo(self):
        #mensagem = "Tere"
        try:
            while True:
                message, client_address = self.server_socket.recvfrom(2048)
                answer = message.upper()
                #print("Vou dormir por 5 segundos");
                #time.sleep(5);
                #print("Parei de dormir");

                self.server_socket.sendto(answer, client_address)

                print 'Pacote recebido de', client_address

        except KeyboardInterrupt:
            self.server_socket.close()

            print 'Servidor encerrado.'


def main():
    transmissor = Transmissor(12000);
    transmissor.enviaArquivo();

    


if __name__ == '__main__':
    main()
