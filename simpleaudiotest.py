

import simpleaudio as sa
import re
import _thread
import time

print('hello')
sound = "AY"
delay = .125

time.sleep(delay)
with open("sounds/"+sound+".wav", mode = "rb") as audio_data:
    audio_data = audio_data.read()
    play_obj = sa.play_buffer(audio_data, 2, 2, 44100)

    play_obj.wait_done()

    play_obj.stop()


