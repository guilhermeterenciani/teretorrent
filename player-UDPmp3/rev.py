#!/usr/bin/python
# coding: utf-8
from socket import *
from pydub import AudioSegment
from pydub.playback import play
import io
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        sock.sendto("luffy.mp3",("localhost",12000))
        while 1:  
            data, server = (sock.recvfrom(65500))
            song = AudioSegment.from_file(io.BytesIO(data), format="mp3")
            play(song) #with pydub
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()