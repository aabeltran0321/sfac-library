# import required module
import os

# play sound
file = "success-221935.mp3"
print('playing sound using native player')
os.system(f"afplay {file} -t 1.8")