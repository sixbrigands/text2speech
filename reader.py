#Based on script by Alex I. Ramirez @alexram1313
#https://github.com/alexram1313/text-to-speech-sample

import simpleaudio as sa
import re
import _thread
import time
from pydub import AudioSegment
from pydub.playback import play
class TextToSpeech:
    
    CHUNK = 1024
    #apparently you can both indicate type (see type hints) and instantiate a variable in the def statement
    #here we point to the txt file that breaks words in to phonemes
    # l = the phoneme strings dict
    # _load_words is the method that parses the CMU dictionary
    def __init__(self, CMUdict:str = 'CMUdict.txt'):
        self._l = {}
        self._load_words(CMUdict)

    def _load_words(self, CMUdict:str):
        with open(CMUdict, 'r') as file:
            print("opened CMU dict!")
            for line in file:
                #ignore comments in txt file
                if not line.startswith(';;;'):
                    #key is the word, val is the string of phonemes, 1st arg = delimiter, 2nd is how many times to split max
                    key, val = line.split('  ',2)
                    #use regex to parse the phonemes in val
                    self._l[key] = re.findall(r"[A-Z]+",val)

    def get_pronunciation(self, str_input):
        phoneme_list = []
        #the following parses the user input (typed words to be spoken)
        #\w is any alphanumeric character. see https://docs.python.org/3/howto/regex.html
        for word in re.findall(r"[\w']+",str_input.upper()):
            if word in self._l:
                phoneme_list += self._l[word]
        print(phoneme_list)
        
        return phoneme_list
    
    #plays wav files using anythingbut pyaudio
    def make_audio(self, phoneme_list):
        full_audio = AudioSegment.empty()
        for phoneme in phoneme_list:
            segment = AudioSegment.from_wav("sounds/"+phoneme+".wav")
            full_audio += segment
        
        return full_audio 
        


    def export_audio(text, audio):
        full_audio.export("mashup.mp3", format="mp3")
        

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        user_input = input('Enter a word or phrase: ')
        phoneme_list = tts.get_pronunciation(user_input)
        audio = tts.make_audio(phoneme_list)
        #audio.export("<FILE PATH HERE FOR EXPORT".wav", format ="wav")
        play(audio)
        