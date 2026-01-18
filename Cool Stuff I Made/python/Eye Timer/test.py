from pygame import mixer
from time import sleep
from random import randint

# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("offsetSong.ogg")

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song
mixer.music.play(-1)

# infinite loop
while True:
    
    
    for i in range(40):
        sleep(10)
        print(40 - i)