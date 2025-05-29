import os
import eel

from main2 import *

import recoganize

from playsound import playsound

def playAssistantSound(sound_path):
    try:
        playsound(sound_path)
    except Exception as e:
        print(f"Error playing sound: {e}")


    

def start():
    
    eel.init(".")

    playAssistantSound(r"C:\Users\vikra\Downloads\jarvis-main\jarvis-main\www\assets\audio\start_sound.mp3")
    # @eel.expose
    # def init():
        # subprocess.call([r'device.bat'])
        # eel.hideLoader()
    flag = recoganize.AuthenticateFace()
        # if flag == 1:
        #     eel.hideFaceAuth()
        #     speak("Face Authentication Successful")
        #     eel.hideFaceAuthSuccess()
        #     speak("Hello, Welcome Sir, How can i Help You")
        #     eel.hideStart()
        #     playAssistantSound()
        # else:
        #     speak("Face Authentication Fail")

    eel.start('index.html', mode=None, host='localhost', block=True)

