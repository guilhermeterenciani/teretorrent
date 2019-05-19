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
        data, cliente = sock.recvfrom(1200);
        print("Recebido requisição do cliente "+cliente[0]+" Do dado= "+data.decode())
        song = AudioSegment.from_file('sender/'+data.decode(), format="mp3")
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(song.sample_width),
                    channels=song.channels,
                    rate=song.frame_rate,
                    output=True)
        print("Audio info: format=%d channels= %d rate= %d"
            %(p.get_format_from_width(song.sample_width),song.channels,song.frame_rate))
        x=0;
        
        lamb = 1.820;
        tamfile=len(song);
        while(x<tamfile):
            if(x+lamb>tamfile):
                print(len(song[x:-1].raw_data));
                sock.sendto(song[x:-1].raw_data,cliente);
            else:
                print(len(song[x:x+lamb].raw_data));
                sock.sendto(song[x:x+lamb].raw_data,cliente);
            x = x+lamb;
            time.sleep(0.0015);
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()