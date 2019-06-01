#!/usr/bin/python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class GeraGraficos:
    """
    classe destinada à geração de gráficos do trabalho
    """

    def __init__(self):
        self.df = pd.read_csv("log/app.log", sep='$')

    def graficoTransmissaoSeq(self, who = 'receptor'):
        '''
        gera o gráfico de transmissão e armazena a saída em png
        who: receptor ou emissor, os logs devem gerar gráficos separados
        '''
        df     = self.df[self.df['pacote'] == 'PKTENVIADO']    #enviado
        dfr    = self.df[self.df['pacote'] == 'PKTRECEBIDO']   #recebido
        dft    = self.df[self.df['pacote'] == 'PKTEXECUTADO']  #executado
        dfdesc = self.df[self.df['pacote'] == 'PKTDESCARTADO'] #descartado

        tempoTotal          = pd.DataFrame()
        tempoTotal["tempo"] = self.df['segundos'] + self.df['milesimos']/100
        
        ######### enviado #########
        npc  = pd.DataFrame(df['npacote'].astype('int64'))

        time1 = pd.DataFrame()
        time1["tempo"] = df['segundos'] + self.df['milesimos']/1000

        #ndf = pd.DataFrame( data = tempoTotal)
        ndf1 = pd.DataFrame( data = time1)
        ndf1['Transmitido'] = npc

        #ndf = ndf.reset_index()
        #del ndf['index']

        ######### enviado #########

        ######### recebido #########
        npcr  = pd.DataFrame(dfr['npacote'].astype('int64'))

        timer = pd.DataFrame()
        timer["tempo"] = dfr['segundos'] + dfr['milesimos']/1000

        ndf2 = pd.DataFrame( data = timer)
        ndf2['Recebido'] = npcr

        ######### enviado #########


        ######### tocados #########
        npct  = pd.DataFrame(dft['npacote'].astype('int64'))

        timet = pd.DataFrame()
        timet["tempo"] = dft['segundos'] + dft['milesimos']/1000

        ndf3 = pd.DataFrame( data = timet)
        ndf3['Tocados'] = npct

        print(ndf3['Tocados'])

        ######### tocados #########


        ######### descartados #########
        npcd  = pd.DataFrame(dfdesc['npacote'].astype('int64'))

        timed = pd.DataFrame()
        timed["tempo"] = dfdesc['segundos'] + dfdesc['milesimos']/1000

        ndf4 = pd.DataFrame( data = timed)
        ndf4['Descartados'] = npcd

        ######### descartados #########


        #ndf = ndf.fillna(0)
        ndf1 = ndf1.dropna()
        ndf2 = ndf2.dropna()
        #ndf3 = ndf2.dropna()
        #ndf4 = ndf2.dropna()

        fig, ax = plt.subplots()

        plt.title( 'Gráfico de transmissão - ' + who.capitalize() )
        plt.ylabel('Número do pacote')

        ndf1.plot.line(x = "tempo", y = "Transmitido", ax = ax)
        ndf2.plot.line(x = "tempo", y = "Recebido", ax = ax)
        ndf3.plot.line(x = "tempo", y = "Tocados", ax = ax)
        ndf4.plot.line(x = "tempo", y = "Descartados", ax = ax)
        plt.show()


        #print(ndf3)
        #print(ndf4)

        fig.savefig('rel_transmissão_'+who+'.png', papertype = 'a4')
        plt.close(fig)


obj = GeraGraficos()
obj.graficoTransmissaoSeq()