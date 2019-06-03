#!/usr/bin/python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class GraphicsGen:
    """
    classe destinada à geração de gráficos do trabalho
    """

    def __init__(self):
        
        self.arquivoenvio1 = pd.read_csv("log/app_envio1.log", sep='$')

        self.arquivoenvio2 = pd.read_csv("log/app_envio2.log", sep='$')


        self.dfrec = pd.read_csv("log/app.log", sep='$')




    def throughputGraphic(self, step = 100):
        PACKET_SIZE = 3561/1024 # to kbps

        dft    = self.dfrec[self.dfrec['pacote'] == 'PKTEXECUTADO']  #executado

        segs = dft['segundos']
        mil  = dft['milesimos']

        grouped = dft.groupby(['minutos', 'segundos'])

        values = []
        time   = []
        
        i = 0
        
        for name, group in grouped:
            antVal  = group['milesimos'].iloc[0]
            lastVal = group['milesimos'].iloc[-1]

            #print('antVal: {} lastVal: {} '.format(antVal, lastVal))
            
            while(antVal <= lastVal):
                interval = group[(group['milesimos']>= (antVal)) & (group['milesimos']< (antVal+step))]
                #interval = group[group['milesimos'].between(antVal, antVal+step)]

                count = len(interval.index)

                values.append(count*PACKET_SIZE)
                time.append( (i*step)/1000.0 )

                i = i + 1
                antVal = antVal + step

                #print( interval )
                #print( 'size: {}, antval: {}, lastVal: {}'.format(count, antVal, lastVal) )
            
        fig, ax = plt.subplots()

        data = {
            'tempo': time,
            'vazao': values
        }

        dfThroughput = pd.DataFrame(data=data)
            
        plt.ylabel('Kbps')
        dfThroughput.plot(x = "tempo", y = "vazao", ax = ax, kind = 'line', style='-' , label='Vazão no receptor - Média: {:.2f} kbps '.format(dfThroughput['vazao'].mean()) )              
        plt.show()

        #print( dft[dft['segundos'] == dft['segundos'].max()] )

        
        fig.savefig('rel_vazao_.png', papertype = 'a4')
        plt.close(fig)

    def transmissionGraphic(self, kind = 'line', style = '-' ):
        '''
        gera o gráfico de transmissão e armazena a saída em png
        kind: tipo de gráfico a visualizar: line, scatter,  opcional
        style: o marcador a ser aplicado (- para linha contínua)
        '''
        
        fig, ax = plt.subplots()

        plt.title( 'Gráfico de transmissão' )

        size = 5
        
        mint     = self.dfrec['minutos'].iloc[0]
        segt     = self.dfrec['segundos'].iloc[0]
        mst      = self.dfrec['milesimos'].iloc[0]

        minutosenviado1 = self.arquivoenvio1['minutos'].iloc[0]
        segudnosenviado1 = self.arquivoenvio1['segundos'].iloc[0]
        mileenviado1 =self.arquivoenvio1['milesimos'].iloc[0]

        minutosenviado2 = self.arquivoenvio2['minutos'].iloc[0]
        segudnosenviado2 = self.arquivoenvio2['segundos'].iloc[0]
        mileenviado2 =self.arquivoenvio2['milesimos'].iloc[0]

        dfmin    = self.dfrec[self.dfrec['minutos'] < mint+3 ]
        dfminarquivoenvio1 = self.arquivoenvio1[self.arquivoenvio1['minutos'] < mint+3 ]
        dfminarquivoenvio2 = self.arquivoenvio2[self.arquivoenvio2['minutos'] < mint+3 ]
        
        dfr    = dfmin[dfmin['pacote'] == 'PKTRECEBIDO' ]   #recebido
        dft    = dfmin[dfmin['pacote'] == 'PKTEXECUTADO']  #executado
        dfdesc = dfmin[dfmin['pacote'] == 'PKTDESCARTADO'] #descartado
        dfrenviado1 = dfminarquivoenvio1[dfminarquivoenvio1['pacote'] == 'PKTENVIADO'  ]
        dfrenviado2 = dfminarquivoenvio2[dfminarquivoenvio2['pacote'] == 'PKTENVIADO'  ]
        #print(self.dfrec)

        #tempoTotal          = pd.DataFrame()
        #tempoTotal["tempo"] = self.df['segundos'] + self.df['milesimos']/100
        
        ######### enviado #########
        try:
            npct12  = pd.DataFrame(dfrenviado1['npacote'].astype('int64'))

            timet = pd.DataFrame()
            timet["tempo"] = (dfrenviado1['minutos']-minutosenviado1)*60 + (dfrenviado1['segundos']-segudnosenviado1) + (dfrenviado1['milesimos']-mileenviado1)/1000

            ndf312 = pd.DataFrame( data = timet)
            ndf312['Enviados'] = npct12

            #print(ndf3)

            ndf312.plot(x = "tempo", y = "Enviados", ax = ax, kind = kind, marker=style,  color='red', label='Enviados Sender1', s=size)
        except:
            print("não foi possível plotar os pacotes tocados")
        
        ######### enviado #########
        ######### enviado #########
        try:
            npct  = pd.DataFrame(dfrenviado2['npacote'].astype('int64'))

            timetere = pd.DataFrame()
            timetere["tempo"] = (dfrenviado2['minutos']-minutosenviado2)*60 + (dfrenviado2['segundos']-segudnosenviado2) + (dfrenviado2['milesimos']-mileenviado2)/1000

            ndf3 = pd.DataFrame( data = timetere)
            ndf3['Enviados1'] = npct

            #print(ndf3)

            ndf3.plot(x = "tempo", y = "Enviados1", ax = ax, kind = kind, marker=style,  color='yellow', label='Enviados Sender2', s=size)
        except:
            print("não foi possível plotar os pacotes tocados")
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

            ndf2.plot(x = "tempo", y = "Recebido", ax = ax, kind = kind, marker=style, color='blue', label='Recebido', s=size)
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

            ndf3.plot(x = "tempo", y = "Tocados", ax = ax, kind = kind, marker=style,  color='green', label='Tocados', s=size)
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

            ndf4.plot(x = "tempo", y = "Descartados", ax = ax, kind = kind, marker=style , color='black', label='Descartados', s=size)
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

#descomente aqui para gerar o gráfico de vazão
obj.throughputGraphic()