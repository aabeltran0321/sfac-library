import os
from playsound import playsound
def play():
    file = "mixkit-classic-short-alarm-993.wav"
    # print('playing sound using native player')
    # os.system(f"afplay {file} -t 1.8")

    playsound(file)
    print('playing sound using  playsound')