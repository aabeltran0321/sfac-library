# import required module
import os
from playsound import playsound

def play():
    # play sound
    file = "mixkit-game-success-alert-2039.wav"
    # print('playing sound using native player')
    # os.system(f"afplay {file} -t 1.8")

    # for playing note.wav file
    playsound(file)
    print('playing sound using  playsound')
