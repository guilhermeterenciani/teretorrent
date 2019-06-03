from random import random
import numpy as np
import math
import matplotlib.pyplot as plt

class RandomDelay:
    """
    cria um delay em segundos a partir de uma variável aleatória criada a partir de uma 
    função exponencial a partir de uma função aleatória uniforme (intervalo de 0 a 2), 
    com média E(x) = 50 (empírico)
    """

    def __init__(self, nElems):
        #f chance de perder um pacote
        self.f = 0.5
        self.elems = range(0,nElems)
        self.vals = []

        f = open("rtt.txt", "r")
        self.rtt = float(f.read())

        #print(self.rtt)

        for x in self.elems:
            self.vals.append(self.rtt/2 + self.exprandom(100))
            #print(self.vals[-1])
        
        #plt.plot(self.vals)
        #plt.title("função exp")
        #plt.show()
    
    def exprandom(self, _lambda):
        """
        monta o vetor de tempos de atraso. NÃO deve ser acessada externamente
        """
        
        #F(x) = u

        u = np.random.uniform(0,0.1)
        #u = fx(_lambda, x)
        
        # X = -((1/_lambda)* log(1-u))
        return - ( (1/_lambda)*math.log(u) )

    def getDelay(self, x):
        """
        determina o tempo de atraso em segundos < 0.2seg
        """
        return self.vals[x]


    def acceptPackage(self):
        """
        determina se um pacote deve ser aceito ou descartado a partir da probabilidade 
        cEntrega de um pacote ser aceito menos a probabilidade f de um pacote ser 
        descartado.
        """
        cEntrega = 1 - np.random.rand()
        return cEntrega > self.f



#r = RandomDelay(5000)
#for x in range (0,100):
#    print(r.getDelay(x))
#    print(r.acceptPackage())