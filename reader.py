#Based on script by Alex I. Ramirez @alexram1313
#https://github.com/alexram1313/text-to-speech-sample

import re
import wave
import pyaudio
import _thread
import time

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
        list_pron = []
        #the following parses the user input (typed words to be spoken)
        #\w is any alphanumeric character. see https://docs.python.org/3/howto/regex.html
        for word in re.findall(r"[\w']+",str_input.upper()):
            if word in self._l:
                list_pron += self._l[word]
        print(list_pron)
        delay=0
        for pron in list_pron:
            _thread.start_new_thread( TextToSpeech._play_audio, (pron,delay,))
            delay += 0.145
    
    #plays wav files using pyaudio
    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            wf = wave.open("sounds/"+sound+".wav", 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            data = wf.readframes(TextToSpeech.CHUNK)
            
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
        
            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass
    
 
 

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        tts.get_pronunciation(input('Enter a word or phrase: '))