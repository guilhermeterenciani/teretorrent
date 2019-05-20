#!/usr/bin/python
# coding: utf-8
from socket import *
from pydub import AudioSegment
from pydub.playback import play
import pyaudio

p = pyaudio.PyAudio()
import io
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(('', 12001))
    stream = p.open(format=8,channels=2,rate=44100,output=True)
    try:
        #sock.sendto("luffy2.mp3".encode('utf-8'),("localhost",12000))
        while 1:  
            data, server = (sock.recvfrom(320))
            stream.write(data);
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()