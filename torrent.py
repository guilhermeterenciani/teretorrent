#!/usr/bin/python
# coding: utf-8
from socket import *
import time
import threading
import _thread
import sys
s = _thread.allocate_lock()
class Torrent(object):
    """docstring for torrent"""
    def __init__(self,nameSender):
        super(Torrent, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.enviar = nameSender;
        self.sock.bind(('', 12000));
        s.acquire()
        s.release()
        #self.sock_files = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
        
        #self.client = socket(AF_INET,SOCK_DGRAM) # UDP
        #self.client.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        #self.client.bind(("", 37020))
        #self.sock_files.bind(("", 44444))
        #self.sock.settimeout(0.2);
        x = threading.Thread(target=self.enviaArquivos,args=(1,));
        x.start()
        y = threading.Thread(target=self.recebeArquivos,args=());
        y.start();

    def enviaArquivos(self,name):
        #self.sock_files.settimeout(0.2)
        message = b"your very important message from->"+ self.enviar.encoder();
        while True:
            s.acquire()
            self.sock.sendto(message, ('<broadcast>', 12000))
            s.release();
            time.sleep(1);

    def recebeArquivos(self):
        while True:
            s.acquire()
            data, addr = self.sock.recvfrom(1024)
            s.release();
            print("received message: %s"%data)
def main():
    if len(sys.argv)<2:
        print("Erro: esperado ./torrent.py  [nomeDoSender]");
        exit();
    torrent = Torrent(sys.argv[1]);

if __name__ == '__main__':
    main()
