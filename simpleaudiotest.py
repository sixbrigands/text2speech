

from pydub import AudioSegment
from pydub.playback import play

print('hello')
phoneme1 = "P"
phoneme2 = "EY"
delay = .125

phoneme1 = AudioSegment.from_wav("sounds/"+phoneme1+".wav")
phoneme2 = AudioSegment.from_wav("sounds/"+phoneme2+".wav")

word = phoneme1 + phoneme2

play(word)