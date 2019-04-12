#!/usr/bin/python
# coding: utf-8
from playsound import playsound
import wave

def main():
    try:
        #pip install playsound
        wf = wave.open('sender/one.wav', 'rb');
        data = wf.readframes(1280);

        print data[0];

        playsound(data[0]);
    except KeyboardInterrupt:
        print("Finalizando programa");


if __name__ == '__main__':
    main()