#!/usr/bin/python
# coding: utf-8
from socket import *
import time
import threading
import _thread
import sys
import glob
import pickle
#usado para inserir em uma lista ordenada;
import bisect 
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s')



#definindo constantes no código:


PACOTE_DIRETORIOS = 0;


enviolock = _thread.allocate_lock()
recebimentolock = _thread.allocate_lock()
class Torrent(object):
    """docstring for torrent"""
    def __init__(self):
        super(Torrent, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.sock.bind(('', 12000));

        #matriz de arquivos com seus seeders;
        #luff.mp3 [10.10.12.100, 10.10.12.10]
        #tiao.mp3 [10.10.12.102, 10.10.12.101]
        #aaaa.mp3 [10.10.12.100, 10.10.12.101, 10.10.12.103, 10.10.12.104]]
        #bbbb.mp3 [10.10.12.12]
        self.listaarquivos = dict();

        try:
            x = threading.Thread(target=self.enviaArquivos,args=(1,));
            x.start()
            y = threading.Thread(target=self.recebeArquivos,args=());
            y.start();
        except KeyboardInterrupt:
            print("Finalizando as threading de envio e recebimento dos arquivos")
            x.stop()
            y.stop()
            self.sock.close()

    def enviaArquivos(self,name):
        
        message = b"your very important message from-> terepc"
        while True:
            try:
                #função pickle usada para transformar o vetor em bytes.
                #depois do outro lado voltamos para vetor.
                #função blob utilizada para listar os arquivos mp3 que existem na pasta sender do meu programa.
                datasender = [];
                datasender.append(PACOTE_DIRETORIOS);
                datasender.append(glob.glob("./sender/*.mp3"))
                data_string = pickle.dumps(datasender);
                #requerindo permissão de escrita no buffer, pois outras threading podem estar utilizando para escrita.
                enviolock.acquire()
                #enviando os dados por broadcast, sempre pela porta 12000
                self.sock.sendto(data_string, ('<broadcast>', 12000))
                #liberando os semaforo.
                enviolock.release();
            except KeyboardInterrupt:
                enviolock.release();
                print("Finalizando threading de enviaArquivos")
            #a função de liberar o arquivo vai ser chamada de 1 em 1 segundo. para enviar por broadcast todos os arquivos que tem na minha máquina.
            time.sleep(1);


    def recebeArquivos(self):
        '''
        função curinga para limpar o dicionário e apagar pessoas que não estão mais na minha rede 
        p2p -> função não foi utilizada porque os peers nunca vão morrer.
        cont = 0
        '''
        while True:
            '''
            função curinga hehehe
            if cont<6000:
                cont = cont+1
            else:
                cont=0;
                self.listaarquivos = dict();
            '''
            recebimentolock.acquire()
            self.sock.settimeout(0.002)
            try:
                
                data, addr = self.sock.recvfrom(1024)
                recebimentolock.release(); #TODO: provavelmente não vai ficar aqui hehehehe
                data_arr = pickle.loads(data);
                print("Recebi do sender= ")
                #print(data_arr);
                #Se a posição zero contiver o pacote_diretorios:
                #Preparamos para atualizar a lista de usuários do nosso seders: "Pessoas que podem me enviar arquivos"
                if(data_arr[0]==PACOTE_DIRETORIOS):
                    for x in data_arr[1]:
                        if x not in self.listaarquivos:
                            self.listaarquivos[x] = [addr[0]];
                        else:
                            if (addr[0] not in self.listaarquivos[x]): 
                               self.listaarquivos[x].append(addr[0]); 
                    print (self.listaarquivos);

                    '''
                    print("Posso começar a atualizar a lista de seeders" + addr[0] +":"+str(addr[1]));
                    for x in data_arr[1]:
                        try:
                            #print (self.listaarquivos[0])
                            if type(self.listaarquivos) is not list:
                                self.listaarquivos.append([x,[addr[0]]]);
                                print("O arquivo vai ser inserido na lista => "+x);
                            index = self.listaarquivos[0].index(x)
                            print("O arquivo ja esta na lista => "+x);
                            #se já for uma lista voce vai adicionar o ip do cara que tem o arquivo;
                            if type(self.listaarquivos[index]) is list:
                                #adicionando o ip que tem este arquivo.
                                self.listaarquivos[index].append(addr[0])
                            else:
                                #ninguém até o momento tinha o arquivo. Agora podemos utiliza-lo;
                                print(index);
                                #self.listaarquivos[index] = [];
                                self.listaarquivos[index].append(addr[0])
                                pass

                        except ValueError:
                    '''

                            
                    print (self.listaarquivos)

            
            except timeout:
                recebimentolock.release();
                pass
                #print("Não recebi dados de outros piers");
            except KeyboardInterrupt:
                recebimentolock.release();
                print("Finalizando o software e a threading de recebimento dos arquivos.");
            
            #print("received message: %s"%data)
    def requisicaodeArquivo(self,nomeArquivo):
        '''
            Função responsável por requisição de arquivos para serem executados pelo programa.
        '''





def main():
    '''
    if len(sys.argv)<2:
        print("Erro: esperado ./torrent.py  [nomeDoSender]");
        exit();
    '''
    torrent = Torrent();

if __name__ == '__main__':
    main()
