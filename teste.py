from pydub import AudioSegment
import pyaudio
import bisect;
from collections import deque
song = AudioSegment.from_file('sender/luffy.mp3', format="mp3",bitrate="128")
tamfile=len(song[0:1000].raw_data);
print(len(song))
print(len(song.raw_data))
print(tamfile)
aux = song[0:1].raw_data
print (len(aux))