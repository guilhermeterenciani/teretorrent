#!/usr/bin/python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class GraphicsGen:
    """
    classe destinada à geração de gráficos do trabalho
    """

    def __init__(self):
        self.dfenv = pd.read_csv("log/app_envio1.log", sep='$')
        self.dfrec = pd.read_csv("log/app.log", sep='$')

    def throughputGraphic(self):
        dft    = self.dfrec[self.dfrec['pacote'] == 'PKTEXECUTADO']  #executado

        segs = dft['segundos']
        mil  = dft['milesimos']

        grouped = dft.groupby('segundos')

        for name, group in grouped:
            count = 0 #10398  11
            antVal = group['milesimos'].iloc[0]

            interval = group[group['milesimos']<= (antVal+100)]

            print( group['milesimos'] )

        #print( dft[dft['segundos'] == dft['segundos'].max()] )

    def transmissionGraphic(self, kind = 'line', style = '-' ):
        '''
        gera o gráfico de transmissão e armazena a saída em png
        kind: tipo de gráfico a visualizar: line, scatter,  opcional
        '''
        
        fig, ax = plt.subplots()

        plt.title( 'Gráfico de transmissão' )
        
        mint     = self.dfrec['minutos'].iloc[0]
        segt     = self.dfrec['segundos'].iloc[0]
        mst      = self.dfrec['milesimos'].iloc[0]
        dfmin    = self.dfrec[self.dfrec['minutos'] < mint+3 ]
        dfminenv = self.dfenv[self.dfenv['minutos'] < mint+3 ]

        

        df     = dfminenv[dfminenv['pacote'] == 'PKTENVIADO'  ]   #enviado
        dfr    = dfmin[dfmin['pacote'] == 'PKTRECEBIDO' ]   #recebido
        dft    = dfmin[dfmin['pacote'] == 'PKTEXECUTADO']  #executado
        dfdesc = dfmin[dfmin['pacote'] == 'PKTDESCARTADO'] #descartado

        print(self.dfrec)

        #tempoTotal          = pd.DataFrame()
        #tempoTotal["tempo"] = self.df['segundos'] + self.df['milesimos']/100
        
        ######### enviado #########
        try:
            npc  = pd.DataFrame(df['npacote'].astype('int64'))

            #print(npc)

            time1 = pd.DataFrame()
            time1["tempo"] = (df['minutos']-mint)*60 + (df['segundos']-segt) + (df['milesimos']-mst)/1000

            #ndf = pd.DataFrame( data = tempoTotal)
            ndf1 = pd.DataFrame( data = time1)
            ndf1['Transmitido'] = npc

            ndf1 = ndf1.dropna()

            #ndf = ndf.reset_index()
            #del ndf['index']

            #ndf1.plot(x = "tempo", y = "Transmitido", ax = ax, kind = kind, marker=style,  linestyle='dashed')
            ndf1.plot(x = "tempo", y = "Transmitido", ax = ax, kind = kind, marker=style, color='red' , label='Transmitido', s=10)    
        except:
            print("não foi possível plotar os pacotes transmitidos")
        
        ######### enviado #########

        ######### recebido #########
        try:
            npcr  = pd.DataFrame(dfr['npacote'].astype('int64'))

            timer = pd.DataFrame()
            timer["tempo"] = (dfr['minutos']-mint)*60 + (dfr['segundos']-segt) + (dfr['milesimos']-mst)/1000

            ndf2 = pd.DataFrame( data = timer)
            ndf2['Recebido'] = npcr

            ndf2 = ndf2.dropna()

            #print(ndf2)

            ndf2.plot(x = "tempo", y = "Recebido", ax = ax, kind = kind, marker=style, color='blue', label='Recebido', s=10)
        except:
            print("não foi possível plotar os pacotes recebidos")

        ######### enviado #########


        ######### tocados #########
        
        try:
            npct  = pd.DataFrame(dft['npacote'].astype('int64'))

            timet = pd.DataFrame()
            timet["tempo"] = (dft['minutos']-mint)*60 + (dft['segundos']-segt) + (dft['milesimos']-mst)/1000

            ndf3 = pd.DataFrame( data = timet)
            ndf3['Tocados'] = npct

            #print(ndf3)

            ndf3.plot(x = "tempo", y = "Tocados", ax = ax, kind = kind, marker=style,  color='green', label='Tocados', s=10)
        except:
            print("não foi possível plotar os pacotes tocados")

        #print(ndf3['Tocados'])

        ######### tocados #########


        ######### descartados #########
        try:
            npcd  = pd.DataFrame(dfdesc['npacote'].astype('int64'))

            timed = pd.DataFrame()
            timed["tempo"] = (dfdesc['minutos']-mint)*60 + (dfdesc['segundos']-segt) + (dfdesc['milesimos']-mst)/1000

            ndf4 = pd.DataFrame( data = timed)
            ndf4['Descartados'] = npcd

            ndf4.plot(x = "tempo", y = "Descartados", ax = ax, kind = kind, marker=style , color='red', label='Descartados', s=10)
        except:
            print("não foi possível plotar os pacotes descartados")

        ######### descartados #########

        plt.ylabel('Número do pacote')
        plt.show()

        fig.savefig('rel_transmissão_.png', papertype = 'a4')
        plt.close(fig)

        #print(mint)


obj = GraphicsGen()

#plot do gráfico sequencial
obj.transmissionGraphic(style='o', kind='scatter')
#obj.throughputGraphic()