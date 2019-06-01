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
        self.df = pd.read_csv("log/app.log", sep='$')

    def throughputGraphic(self):
        dft    = self.df[self.df['pacote'] == 'PKTEXECUTADO']  #executado

        segs = dft['segundos']
        mil  = dft['milesimos']

        grouped = dft.groupby('segundos')

        for name, group in grouped:
            count = 0 #10398  11
            antVal = group['milesimos'].iloc[0]

            interval = group[group['milesimos']<= (antVal+100)]

            print( group['milesimos'] )

        #print( dft[dft['segundos'] == dft['segundos'].max()] )

    def transmissionGraphic(self, who = 'receptor', kind = 'line' ):
        '''
        gera o gráfico de transmissão e armazena a saída em png
        who: receptor ou emissor, os logs devem gerar gráficos separados, opcional
        kind: tipo de gráfico a visualizar: line, scatter,  opcional
        '''
        mint   = self.df['minutos'].min()
        dfmin  = self.df[self.df['minutos'] == mint ]

        df     = dfmin[dfmin['pacote'] == 'PKTENVIADO'  ]   #enviado
        dfr    = dfmin[dfmin['pacote'] == 'PKTRECEBIDO' ]   #recebido
        dft    = dfmin[dfmin['pacote'] == 'PKTEXECUTADO']  #executado
        dfdesc = dfmin[dfmin['pacote'] == 'PKTDESCARTADO'] #descartado

        tempoTotal          = pd.DataFrame()
        tempoTotal["tempo"] = self.df['segundos'] + self.df['milesimos']/100
        
        ######### enviado #########
        npc  = pd.DataFrame(df['npacote'].astype('int64'))

        time1 = pd.DataFrame()
        time1["tempo"] = df['segundos'] + df['milesimos']/1000

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

        #print(ndf3['Tocados'])

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
        

        fig, ax = plt.subplots()

        plt.title( 'Gráfico de transmissão - ' + who.capitalize() )
        plt.ylabel('Número do pacote')

        ndf1.plot(x = "tempo", y = "Transmitido", ax = ax, kind = kind)
        ndf2.plot(x = "tempo", y = "Recebido", ax = ax, kind = kind)
        ndf3.plot(x = "tempo", y = "Tocados", ax = ax, kind = kind)
        ndf4.plot(x = "tempo", y = "Descartados", ax = ax, kind = kind)
        plt.show()

        fig.savefig('rel_transmissão_'+who+'.png', papertype = 'a4')
        plt.close(fig)

        print(mint)


obj = GraphicsGen()

#plot do gráfico sequencial
obj.transmissionGraphic()
#obj.throughputGraphic()