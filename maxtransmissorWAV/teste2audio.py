#!/usr/bin/python3
# coding: utf-8
from playsound import playsound
import wave
import pyaudio

#https://cadernodelaboratorio.com.br/2017/03/20/lendo-arquivos-wav-utilizando-o-python/
#https://cadernodelaboratorio.com.br/2018/09/03/reproducao-de-arquivos-wave-em-python/

#se o pip3 install pyaudio falhar, siga a thread abaixo.
#https://stackoverflow.com/questions/32879614/having-trouble-installing-pyaudio-for-python3-on-mint

def playfile():
 
    # chunck mostra quantos pontos iremos ler por vez no arquivo wave       
    chunck = 2048  
     
    # abrimos um arquivo wave. O nome do arquivo está na variável self.filename
    wavfile = wave.open( 'sender/sample.wav' , 'rb')
 
    # criamos um objeto pyaudio que ir'manipular o dados lidos do arquivo wav
    audioobj = pyaudio.PyAudio()
 
 
    # criamos um fluxo de áudio. os dados para a geração do do fluxo são obtidos
    # a partir do próprio arquivo wave aberto anteriormente
    stream = audioobj.open(
       format=audioobj.get_format_from_width(wavfile.getsampwidth()),
       channels=wavfile.getnchannels(),
       rate=wavfile.getframerate(),
       output=True)
 
    # lemos <chunck> bytes por vez do stream e o enviamos <write> para o dispositivo
    # padrão de saída de audio. Quando termina de ler sai fora do loop
     
    flagfim = False
 
    while flagfim is False:
        data = wavfile.readframes(chunck)
        if len(data) < chunck:
            flagfim = True
        else:
            stream.write(data)
 
    # para de enviar o fluxo para o dispositivo de saida
    stream.stop_stream()
    #fecha o fluxo
    stream.close()
    # libera os recursos dedicados ao obj de audio
    audioobj.terminate()
    # fecha o arquivo wave
    wavfile.close()

if __name__ == '__main__':
    playfile()