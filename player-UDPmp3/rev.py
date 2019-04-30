#!/usr/bin/python
# coding: utf-8
from socket import *
from pydub import AudioSegment
from pydub.playback import play
import pygame
from pygame.locals import *
import io
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        sock.sendto("luffy2.mp3",("localhost",12000))
        #AudioSegment.converter = which("ffmpeg")
        i = 0;
        datarecv = '';
        while 1:  
            data, server = (sock.recvfrom(3200))
            #print data
            datarecv += data
            #song.set_frame_rate(3200)
            with open('receber.mp3', 'wb') as infile:
                infile.write(data)

            i=i+1;
            datarecv += data
            if(i%1==0):
                #print("Datarecv"+datarecv+'\n')
                i=0
                song = AudioSegment.from_mp3('receber.mp3')

                '''
                pygame.init()
                musica = pygame.mixer.Sound(datarecv)
                musica.set_volume(1.0)
                musica.play(-1)
                musica.stop()
                '''
                datarecv = ''
                play(song);
    except KeyboardInterrupt:
        print("Finalizando programa");

if __name__ == '__main__':
    main()