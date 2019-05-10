#!/usr/bin/python
# coding: utf-8
import wave
from socket import *
import time
from pydub import AudioSegment
import pyaudio
from pydub.playback import play

def main():
    

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 12000))
    try:
        #data, cliente = sock.recvfrom(1200);
        #print("Recebido requisição do cliente "+cliente[0]+" Do dado= "+data.decode())
        
        #Abre o arquivo no formato mp3 ps: só aceita mp3
        #print('sender/'+data.decode()+'\n')
        song = AudioSegment.from_file("sender/NIN.mp3",format="mp3")#(sender/'+data.decode(), format="mp3")
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(song.sample_width),
                    channels=song.channels,
                    rate=song.frame_rate,
                    output=True)
        print("Audio info: format=%d channels= %d rate= %d"
            %(p.get_format_from_width(song.sample_width),song.channels,song.frame_rate))
        fileSize = len(song.raw_data)
        chunkSize = 320
        #stream.write(song.raw_data[6000000:11150000])
        for piece in range(0, fileSize, chunkSize):
            print(len(song.raw_data[piece:piece+chunkSize]))
            stream.write(song.raw_data[piece:piece+chunkSize])

    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()