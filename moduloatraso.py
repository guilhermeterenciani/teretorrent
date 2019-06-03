import threading
import pickle
from randomdelay import RandomDelay
from socket import *
import time
import _thread
import logging
class ModuloAtraso(object):
    """docstring for ModuloAtraso"""
    def __init__(self):
        super(ModuloAtraso, self).__init__()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET,SO_BROADCAST, 1)
        self.sock.bind(('', 12001));
        self.sock.settimeout(2)
        y = threading.Thread(target=self.recebeArquivos,args=());
        y.daemon = True
        y.start();
        self.lista_senders = dict();
        self.enviolock = _thread.allocate_lock()
        self.lognum = 1
        self.listoflogins = dict();

    
    def recebeArquivos(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(3553)
                data_arr = pickle.loads(data);
                #pacote = data_arr[1];
                if addr[0] not in self.lista_senders:
                    self.lista_senders[addr[0]] = [RandomDelay(data_arr[2]),self.lognum]
                    logFile= "./log/app_envio"+str(self.lognum)+".log"
                    print(logFile)
                    f = open(logFile, "w")
                    f.write("hora$minutos$segundos$milesimos$npacote$pacote$quemenviou\n")
                    f.close()                            
                    
                    logger=logging.getLogger(__name__)  #__name__ é uma variável que contem o nome do módulo. Assim, saberemos que módulo emitiu a mensagem
                    logger.setLevel(logging.INFO)
                    logger_handler = logging.FileHandler(logFile, mode='a')
                    logger_handler.setLevel(logging.INFO)
                    logger_formatter = logging.Formatter('%(asctime)s%(msecs)03d$%(message)s','%H$%M$%S$')
                    logger_handler.setFormatter(logger_formatter)
                    logger.addHandler(logger_handler)
                    self.listoflogins[self.lognum] = logger;
                    self.lognum = self.lognum+1;
                
                y = self.lista_senders[addr[0]][0];
                self.listoflogins[self.lista_senders[addr[0]][1]].info(str(data_arr[1]) + '$PKTENVIADO')
                if(y.acceptPackage()):
                    #data_string = pickle.dumps(data_arr);
                    #print("Pacote %d foi aceito com o deley de %f"%(pacote,y.getDelay(pacote)));
                    threadingenvio = threading.Thread(target=self.enviaPacote,args=(data,y.getDelay(data_arr[1])));
                    threadingenvio.daemon = True
                    threadingenvio.start();
                else:
                    #print("Pacote %d foi descartado"% pacote)
                    pass
            except timeout:
                #print("Modulo de Atraso não recebeu pacotes ainda.");
                pass
    def enviaPacote(self,pacote,atraso):
        time.sleep(atraso);
        self.enviolock.acquire()
        self.sock.sendto(pacote,('localhost',12000))
        self.enviolock.release()
