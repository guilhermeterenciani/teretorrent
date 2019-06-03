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
from collections import deque
import numpy as np
import random

from pydub import AudioSegment
import pyaudio
from moduloatraso import ModuloAtraso;

f = open("log/app.log", "w")
f.write("hora$minutos$segundos$milesimos$npacote$pacote$quemenviou\n")
f.close()

logging.basicConfig(filename='log/app.log', filemode='a', level=logging.INFO, format='%(asctime)s%(msecs)03d$%(message)s',datefmt='%H$%M$%S$')

#definindo constantes no código:
PACOTE_DIRETORIOS = 0;
PACOTE_REQUISICAO_DOWNLOAD = 1;
PACOTE_PLAY_AUDIO = 2;
PACOTE_REQUISICAO_DOWNLOAD_FALTANTES = 3;

#Modulo de atraso no envio dos pacotes.
MODULO_ATRASO = True;

enviolock = _thread.allocate_lock()
recebimentolock = _thread.allocate_lock()
player_mp3_lock = _thread.allocate_lock()
logginglock = _thread.allocate_lock()
class Torrent(object):
    """docstring for torrent"""
    def __init__(self):
        super(Torrent, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.sock.bind(('', 12000));
        self.sock.settimeout(0.0002)
        #matriz de arquivos com seus seeders;
        #luff.mp3 [10.10.12.100, 10.10.12.10]
        #tiao.mp3 [10.10.12.102, 10.10.12.101]
        #aaaa.mp3 [10.10.12.100, 10.10.12.101, 10.10.12.103, 10.10.12.104]]
        #bbbb.mp3 [10.10.12.12]
        self.listaarquivos = dict();
        self.data_to_play = deque()
        self.data_key_to_play = deque()
        self.tamfileplay = 400;
        self.ultimopcttocado = 0;
        self.buffersize=2;#porcentagem do arquivo que será buffer.
        p = pyaudio.PyAudio()
        self.stream = p.open(format=8,channels=2,rate=44100,output=True)
        self.moduloatraso = ModuloAtraso();
        try:
            x = threading.Thread(target=self.enviaArquivos,args=(1,));
            x.daemon = True
            x.start()
            y = threading.Thread(target=self.recebeArquivos,args=());
            y.daemon = True
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
            except timeout:
                enviolock.release();
                print("Deu algum erro inesperado na função de enviar arquivos");
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
            try:
                data, addr = self.sock.recvfrom(3553)
                recebimentolock.release(); #TODO: provavelmente não vai ficar aqui hehehehe
                data_arr = pickle.loads(data);
                #print("Recebi do sender= %s o pacote de %d"%(addr[0],data_arr[0]))
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
                    #mensagem de debug para os arquivos.
                    #print (self.listaarquivos);
                elif(data_arr[0]==PACOTE_REQUISICAO_DOWNLOAD):
                    '''
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
                    '''
                    threadingdownload = threading.Thread(target=self.envia_arquivo_para_cliente,args=(data_arr[1],addr,));
                    threadingdownload.start()
                    
                elif(PACOTE_PLAY_AUDIO==data_arr[0]):
                    '''
                        Função para executar os arquivos que chegam no lado do receptor;
                    '''
                    try:
                        #sock.sendto("luffy2.mp3".encode('utf-8'),("localhost",12000))
                        #self.stream.write(data_arr[3]);
                        logginglock.acquire()
                        logging.info("%d$PKTRECEBIDO",data_arr[1])
                        logginglock.release()

                        player_mp3_lock.acquire()
                        if data_arr[1] in self.data_key_to_play:
                            #print("Dado já foi recebido");
                            pass
                        else:
                            
                            if data_arr[1]<=self.ultimopcttocado:
                                #Se é para inserir na posição zero é porque o player já passou desse arquivo.
                                #print("%d PKT foi descartado pois já não será executado pelo player"%data_arr[1])
                                logginglock.acquire()
                                logging.info("%d$PKTDESCARTADO"%data_arr[1])
                                logginglock.release()
                            else:
                                insertposition = bisect.bisect(self.data_key_to_play,data_arr[1])
                                #print("%d PKT foi colocado na fila do player e será executado"%data_arr[1])
                                #print(data_arr[3])
                                self.tamfileplay = data_arr[2]
                                logginglock.acquire()
                                logging.info("%d$PKTRECEBIDOFILA"%data_arr[1])
                                logginglock.release()
                                self.data_to_play.insert(insertposition,data_arr[3])
                                self.data_key_to_play.insert(insertposition,data_arr[1]);
                        player_mp3_lock.release()
                    except KeyboardInterrupt:
                        print("Finalizando programa");
                    
                    #logging.info('Função de recebimento ainda não implementada');
                    #print("Função de recebimento ainda não implementada")
                elif PACOTE_REQUISICAO_DOWNLOAD_FALTANTES==data_arr[0]:
                    threadingdownload = threading.Thread(target=self.envia_arquivo_para_cliente,args=(data_arr[1],addr,data_arr[2],));
                    threadingdownload.start()


            except timeout:
                recebimentolock.release();
                #print("Estouro de timeout do recebimento de arquivos");
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
        datasender = [];
        datasender.append(PACOTE_REQUISICAO_DOWNLOAD);
        datasender.append(nomeArquivo)
        self.arquivo_to_play = nomeArquivo;
        data_string = pickle.dumps(datasender);
        player_mp3_lock.acquire()
        self.data_to_play = deque()
        self.data_key_to_play = deque()
        player_mp3_lock.release()
        #requerindo permissão de escrita no buffer, pois outras threading podem estar utilizando para escrita.
        
        #enviando os pedido de file para todos os serves que contem o arquivo, sempre pela porta 12000
        for server in self.listaarquivos[("./sender/"+nomeArquivo)]:
            print("Pedindo arquivo par o server"+server);
            enviolock.acquire()
            self.sock.sendto(data_string, (server, 12000))
            enviolock.release()
        self.ultimopcttocado = -1;
        self.thread_player = threading.Thread(target=self.play,args=());
        self.thread_player.start()
    def requisicaodeArquivosFaltantes(self,nomeArquivo,listaFaltantes):
        '''
            Função responsável por requisição de pacotes perdidos para serem executados pelo programa.
        '''
        serverstam =len(self.listaarquivos[("./sender/"+nomeArquivo)])
        if serverstam ==1:
            datasender = [];
            datasender.append(PACOTE_REQUISICAO_DOWNLOAD_FALTANTES);
            datasender.append(nomeArquivo)
            datasender.append(listaFaltantes)
            data_string = pickle.dumps(datasender);

            for server in self.listaarquivos[("./sender/"+nomeArquivo)]:
                print("Pedindo arquivo par o server"+server);
                print(listaFaltantes)
                enviolock.acquire()
                self.sock.sendto(data_string, (server, 12000))
                enviolock.release()
        else:
            aux = 2;
            for server in self.listaarquivos[("./sender/"+nomeArquivo)]:
                datasender = [];
                datasender.append(PACOTE_REQUISICAO_DOWNLOAD_FALTANTES);
                datasender.append(nomeArquivo)
                datasender.append(listaFaltantes[::aux])
                data_string = pickle.dumps(datasender);
                print("Pedindo arquivo par o server"+server);
                enviolock.acquire()
                self.sock.sendto(data_string, (server, 12000))
                enviolock.release()
                aux = aux+1
    def envia_arquivo_para_cliente(self,namefile,addr,faltantes=[]):
        song = AudioSegment.from_file('sender/'+namefile, format="mp3")
        lamb = 20;
        tamfile=len(song);
        npacotes = tamfile//20; #TODO Testar isso aqui.
        if (tamfile%20!=0):
            npacotes = npacotes+1;
        if len(faltantes) == 0:
            x=0;
            while(x*lamb<tamfile):
                if np.random.rand()>0.2:
                    if(x*lamb+lamb>tamfile):
                        datasender = [];
                        datasender.append(PACOTE_PLAY_AUDIO);
                        datasender.append(x);
                        datasender.append(npacotes)
                        datasender.append(song[x:-1].raw_data)
                        data_string = pickle.dumps(datasender);
                        enviolock.acquire()
                        if MODULO_ATRASO:
                            self.sock.sendto(data_string,(addr[0],12001));
                        else:
                            self.sock.sendto(data_string,addr);
                        enviolock.release()
                    else:
                        datasender = [];
                        datasender.append(PACOTE_PLAY_AUDIO);
                        datasender.append(x);
                        datasender.append(npacotes)
                        datasender.append(song[x*lamb:x*lamb+lamb].raw_data)
                        data_string = pickle.dumps(datasender);
                        enviolock.acquire()

                        if MODULO_ATRASO:
                            self.sock.sendto(data_string,(addr[0],12001));
                        else:
                            self.sock.sendto(data_string,addr);
                        enviolock.release()
                    logginglock.acquire()
                    logging.info('%d$PKTENVIADO',x);
                    logginglock.release()
                    #logging.error('This will get logged to a file')
                    #print("Enviei o pacote %d"%x)
                    #if len(pickle.dumps(datasender))>349:
                    #    print(len(pickle.dumps(datasender)))
                    x = x+1;
                time.sleep(0.02);
        else:
            for cont in faltantes:
                datasender = [];
                datasender.append(PACOTE_PLAY_AUDIO);
                datasender.append(cont);
                datasender.append(npacotes)
                datasender.append(song[cont*lamb:cont*lamb+lamb].raw_data)
                data_string = pickle.dumps(datasender);
                enviolock.acquire()

                if MODULO_ATRASO:
                    self.sock.sendto(data_string,(addr[0],12001));
                else:
                    self.sock.sendto(data_string,addr);
                enviolock.release()
                logginglock.acquire()
                logging.info('%d$PKTENVIADO',cont);
                logginglock.release()
                time.sleep(0.02);
        del song   
    def __del__(self):
        print("Matando meu objeto");
    def play(self):
        erro = 0;
        loop = True
        while loop:
            player_mp3_lock.acquire();
            #TODO Programar aqui a politica de espera quando der erro.
            tamkeys = len(self.data_key_to_play)
            #se não tiver nenhuma chave no play significa que não tem pacotes para serem tocados
            if tamkeys==0:
                player_mp3_lock.release();
                print("Buffering...");
                if self.tamfileplay ==0:
                    self.tamfileplay = 10;
                #calculando o tamanho do buffer. Está passado no init da classe.
                buffer = (self.tamfileplay*self.buffersize)//100;
                logginglock.acquire()
                logging.info("$PAUSEBUFFERING")
                logginglock.release()
                #tamfaltanteanterior é a quandidade de pacotes que ainda faltam para encher o buffer
                #no inicio é considerado o tamanho do arquivo. Pois é maior que o buffer.
                tamfaltantesanterior = self.tamfileplay
                
                while True:
                    if self.ultimopcttocado + buffer <= self.tamfileplay:
                        player_mp3_lock.acquire();
                        listfaltantes = set(list(range(self.ultimopcttocado+1,self.ultimopcttocado+buffer))).difference(self.data_key_to_play)
                        player_mp3_lock.release();
                    else:
                        player_mp3_lock.acquire();
                        listfaltantes = set(list(range(self.ultimopcttocado+1,self.tamfileplay))).difference(self.data_key_to_play)
                        player_mp3_lock.release();
                    tamfaltantes = len(listfaltantes);
                    print("tambuffer = %d e faltantes = %d"%(buffer,tamfaltantes))
                    if tamfaltantes==0:
                        break
                    elif tamfaltantes < tamfaltantesanterior:
                        aux = list(listfaltantes)
                        random.shuffle(aux)
                        self.requisicaodeArquivosFaltantes(self.arquivo_to_play,aux[:50])
                        time.sleep(5);
                    else:
                        aux = list(listfaltantes)
                        random.shuffle(aux)
                        self.requisicaodeArquivosFaltantes(self.arquivo_to_play,aux[:100])
                        time.sleep(10);
                    tamfaltantesanterior = tamfaltantes;
                logginglock.acquire()
                logging.info("$PLAYBUFFERING")
                logginglock.release()
                
            else:
                erro = 0;
                x = self.data_key_to_play.popleft()
                aux = self.data_to_play.popleft()
                player_mp3_lock.release();
                if (x < self.ultimopcttocado):
                    print("%d$PKTPLAYJAEXECUTOUPOSTERIO"%(x))
                else:
                    #print("%d PKT player"%(x))
                    logginglock.acquire()
                    logging.info("%d$PKTEXECUTADO"%x)
                    logginglock.release()
                    #time.sleep(0.02)
                    #print("%d - Quantidade de pacotes na fila"%(tamkeys))
                    self.stream.write(aux);
                    self.ultimopcttocado = x;
def main():
    '''
    if len(sys.argv)<2:
        print("Erro: esperado ./torrent.py  [nomeDoSender]");
        exit();
    '''
    torrent = Torrent();
    time.sleep(5)
    #torrent.requisicaodeArquivo("luffy.mp3");

if __name__ == '__main__':
    main()
