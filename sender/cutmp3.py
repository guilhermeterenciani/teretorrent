#!/usr/bin/python
# coding: utf-8
import sys
chuck = int(sys.argv[1]);
with open("luffy.mp3",'rb') as f:
    leitura = f.read(chuck)
    with open("test.mp3",'wb') as test:
        test.write(leitura);

print("Finalizando");