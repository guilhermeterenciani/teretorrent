from pydub import AudioSegment
import pyaudio
import time;
p = pyaudio.PyAudio()
from pydub.playback import play
import io

#Open File to get infos from that
song = AudioSegment.from_file("sender/luffy2.mp3", format="mp3")

# open stream based on the wave object which has been input.
stream = p.open(format=p.get_format_from_width(song.sample_width),
                channels=song.channels,
                rate=song.frame_rate,
                output=True)

#data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

'''
with open('file.mp3', 'rb') as fd:
            while True:
            #Take a piece of 320 bytes
                chunk = fd.read(44100)
            #If reach the end of the file
                if not chunk:
                     break
                stream.write(chunk)

            #Return to the beggin
            fd.seek(0)
            fd.close()
'''


#y = 1000
#for x in range(0, 10000000):
 # writing to the stream is what *actually* plays the sound.
try:
    #print(len(song));

    #for x in (0,len(song),1):
    #x=0;
    #lamb = 1.820;
    #while(x<5000):
    #    print(len(song[x:x+lamb].raw_data));
     #   stream.write(song[x:x+lamb].raw_data)
    #    x = x+lamb;
    fileSize = len(song.raw_data)
    chunkSize = 320
    stream.write(song.raw_data[6000000:11150000])
    #for piece in range(0, fileSize, chunkSize):
        #print(len(song.raw_data[piece:piece+chunkSize]))
        #stream.write(song.raw_data[piece:piece+chunkSize])

    # cleanup stuff.
    stream.stop_stream()
    stream.close()
except KeyboardInterrupt:
    print("Finalizando programa");
    stream.stop_stream()
    stream.close()

    p.terminate()
#	y = y+320


# play stream (looping from beginning of file to the end)
#while data != '':
#    
#    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes


# cleanup stuff.
stream.stop_stream()
stream.close()

p.terminate()
