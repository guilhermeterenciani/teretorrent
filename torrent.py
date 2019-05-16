#!/usr/bin/python
# coding: utf-8
from socket import *
import time
import threading

class Torrent(object):
    """docstring for torrent"""
    def __init__(self):
        super(Torrent, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('', 12000));

        self.sock_files = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
        self.sock_files.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.client = socket(AF_INET,SOCK_DGRAM) # UDP
        self.client.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.client.bind(("", 37020))

        x = threading.Thread(target=self.enviaArquivos,args=(1,));
        x.start()
        y = threading.Thread(target=self.recebeArquivos,args=());
        y.start();

    def enviaArquivos(self,name):
        self.sock_files.settimeout(0.2)
        self.sock_files.bind(("", 44444))
        message = b"your very important message"
        while True:
            self.sock_files.sendto(message, ('<broadcast>', 37020))
            time.sleep(1);

    def recebeArquivos(self):
        while True:
            data, addr = self.client.recvfrom(1024)
            print("received message: %s"%data)
def main():
    torrent = Torrent();

if __name__ == '__main__':
    main()