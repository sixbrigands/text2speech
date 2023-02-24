#Based on script by Alex I. Ramirez @alexram1313
#https://github.com/alexram1313/text-to-speech-sample

import simpleaudio as sa
import re
import _thread
import time
from pydub import AudioSegment
import os
# from pydub.playback import play
import vlc

class TextToSpeech:
    
    CHUNK = 1024
    #apparently you can both indicate type (see type hints) and instantiate a variable in the def statement
    #here we point to the txt file that breaks words in to phonemes
    # l = the phoneme strings dict
    # _load_words is the method that parses the CMU dictionary
    def __init__(self, CMUdict:str = 'CMUdict.txt'):
        self._l = {}
        self._load_words(CMUdict)
        self.diphone_dict = {}
        self._load_diphones()
        

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
    
    #plays wav files using anything but pyaudio
    def make_audio(self, phoneme_list):
        full_audio = AudioSegment.empty()
        last_was_diphone = False
        for i in range(len(phoneme_list)):
            if last_was_diphone:
                last_was_diphone = False
                continue
            phoneme = phoneme_list[i]
            if i+ 1 < len(phoneme_list) and phoneme in self.diphone_dict and phoneme_list[i+1] in self.diphone_dict[phoneme]:
                next_phoneme = phoneme_list[i+1]
                diphone_file = f"sounds/diphones/{phoneme}_{next_phoneme}.wav"
                segment = AudioSegment.from_wav(diphone_file)
                last_was_diphone = True
            else:
                phoneme_file = f"sounds/phonemes/{phoneme}.wav"
                segment = AudioSegment.from_wav(phoneme_file)
            full_audio += segment
        
        return full_audio 
        
    # Load diphones in the dir into a dict with starting consonant as the key and a list of vowels following that consonant as the value    
    def _load_diphones(self):
        filename_list = os.listdir("sounds/diphones")
        for filename in filename_list:
            string_without_filetype = filename.replace(".wav", "")
            both_phonemes = string_without_filetype.split("_")
            if both_phonemes[0] in self.diphone_dict:
                self.diphone_dict[both_phonemes[0]].append(both_phonemes[1])
            else:
                self.diphone_dict[both_phonemes[0]] = [both_phonemes[1]]

    def export_audio(text, audio):
        audio.export("mashup.mp3", format="mp3")
        

if __name__ == '__main__':
    tts = TextToSpeech()
    while True:
        user_input = input('Enter a word or phrase: ')
        phoneme_list = tts.get_pronunciation(user_input)
        if len(phoneme_list) > 0:
            audio = tts.make_audio(phoneme_list)
            audio.export("output/output.wav", format ="wav")
            player = vlc.MediaPlayer("output/output.wav")
            player.play()
            # play(audio)
        else:
            print("I couldn't pronounce \"" + user_input + "\"")
        