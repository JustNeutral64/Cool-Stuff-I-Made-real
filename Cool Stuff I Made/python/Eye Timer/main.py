from pygame import mixer
from time import sleep
from random import randint
sleep(50)
# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("beep.mp3")

# Setting the volume
mixer.music.set_volume(0.5)

# Start playing the song
mixer.music.play()

# infinite loop
while True:
    
    # Loading the song
    mixer.music.load("blindEnd.wav")

    # Setting the volume
    mixer.music.set_volume(0.5)

    # Start playing the song
    mixer.music.play()
    
    """
    sleep(11.9)
    mixer.music.stop()
    
    # Loading the song
    mixer.music.load("blindStart.wav")

    # Setting the volume
    mixer.music.set_volume(0.7)

    # Start playing the song
    mixer.music.play()
    """
    
    for i in range(40):
        sleep(10)
        print(i)