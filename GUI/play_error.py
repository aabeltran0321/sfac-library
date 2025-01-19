# import required module
import os

# play sound
file = "mixkit-alert-alarm-1005.wav"
print('playing sound using native player')
os.system(f"afplay {file} -t 1.8")