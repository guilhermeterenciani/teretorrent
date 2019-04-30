#!/usr/bin/python
# coding: utf-8
import wave
from socket import *
import time
from pydub import AudioSegment

def main():
    

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 12000))
    try:
        data, cliente = sock.recvfrom(1200);
        print("Recebido requisição do cliente "+cliente[0]+" Do dado= "+data)
        '''
        with open('sender/'+data, 'rb') as infile:
            d = infile.read(320)
            while d :
                time.sleep(0.1)
                sent = sock.sendto(d,cliente)
                d = infile.read(320)
        '''
        sound = AudioSegment.from_mp3('sender/'+data)

        # len() and slicing are in milliseconds
        end = len(sound);
        pct = 0;
        recorte = sound[0:1]
        print len(recorte)
        recorte.export('new.mp3', format='mp3')


        with open('new.mp3', 'rb') as infile:
            d = infile.read(320)
            while d :
                time.sleep(0.1)
                sent = sock.sendto(d,cliente)
                d = infile.read(320)
        
        #sent = sock.sendto(d.raw_data,cliente)

        # Concatenation is just adding
        #second_half_3_times = second_half + second_half + second_half
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()