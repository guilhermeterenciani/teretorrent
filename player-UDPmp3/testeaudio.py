#!/usr/bin/python
# coding: utf-8
import wave
from socket import *
import time

def main():
    

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 12000))
    try:
        data, cliente = sock.recvfrom(1200);
        print("Recebido requisição do cliente "+cliente[0]+" Do dado= "+data)
        with open('sender/'+data, 'rb') as infile:
            d = infile.read(65500)
            while d :
                time.sleep(1)
                sent = sock.sendto(d,cliente)
                d = infile.read(65500)
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()