#!/usr/bin/python
# coding: utf-8
from socket import *
import time
import threading
import _thread
import sys
import glob
import pickle
s = _thread.allocate_lock()
class Torrent(object):
    """docstring for torrent"""
    def __init__(self):
        super(Torrent, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.sock.bind(('', 12000));
        s.acquire()
        s.release()
        #self.sock_files = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
        
        #self.client = socket(AF_INET,SOCK_DGRAM) # UDP
        #self.client.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        #self.client.bind(("", 37020))
        #self.sock_files.bind(("", 44444))
        #self.sock.settimeout(0.2);
        try:
            x = threading.Thread(target=self.enviaArquivos,args=(1,));
            x.start()
            y = threading.Thread(target=self.recebeArquivos,args=());
            y.start();
        except KeyboardInterrupt:
            print("Finalizando as threading de envio e recebimento dos arquivos")
            x.stop()
            y.stop()

    def enviaArquivos(self,name):
        self.sock.settimeout(0.2)
        message = b"your very important message from-> terepc"
        while True:
            s.acquire()
            try:
                data_string = pickle.dumps(glob.glob("./sender/*.mp3"));
                self.sock.sendto(data_string, ('<broadcast>', 12000))
            except KeyboardInterrupt:
                print("Finalizando threading de enviaArquivos")
            s.release();
            time.sleep(2);


    def recebeArquivos(self):
        while True:
            s.acquire()
            try:
                data, addr = self.sock.recvfrom(1024)
                data_arr = pickle.loads(data);
                print("Recebi do sender= ")
                print(data_arr);
            
            except timeout:
                print("Não recebi dados de outros piers");
            except KeyboardInterrupt:
                print("Finalizando o software e a threading de recebimento dos arquivos.");
            s.release();
            print("received message: %s"%data)
def main():
    '''
    if len(sys.argv)<2:
        print("Erro: esperado ./torrent.py  [nomeDoSender]");
        exit();
    '''
    torrent = Torrent();

if __name__ == '__main__':
    main()
