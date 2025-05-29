import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pickle
import numpy as np
import psutil 
import subprocess
import pygetwindow as gw
import pyautogui
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pythoncom 
from datetime import datetime
import re
import threading
import pywhatkit
from googletrans import Translator
import eel
import recoganize

from playsound import playsound

def playAssistantSound(sound_path):
    try:
        playsound(sound_path)
    except Exception as e:
        print(f"Error playing sound: {e}")
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)
with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

# Start Eel app
eel.init(".")
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine
@eel.expose
def speak(text):
    print(f"JARVIS: {text}")
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
def write_note():
    speak("What should I write in the note?")
    note_content =command()
    if note_content == "None":
        speak("I didn't catch that.")
        return

    filename = f"Note_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, 'w') as file:
        file.write(note_content)

    speak(f"Note saved as {filename}")
    os.system(f"notepad {filepath}")
def cal_day():
    day = datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week
@eel.expose
def wishMe():
    hour = int(datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Vikram, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Vikram, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Vikram, it's {day} and the time is {t}")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        command = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {command}\n")
    except Exception as e:
        speak("Say that again please")
        return "None"
    return command
def write_note():
    speak("What should I write in the note?")
    note_content = command()
    if note_content == "None":
        speak("I didn't catch that.")
        return

    filename = f"Note_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, 'w') as file:
        file.write(note_content)

    speak(f"Note saved as {filename}")
    os.system(f"notepad {filepath}")
def calculate(command):
    command = command.lower()

    # Phrase replacements (important to do these FIRST)
    command = command.replace("multiplied by", "*")
    command = command.replace("divided by", "/")
    command = command.replace("power of", "**")
    command = command.replace("to the power of", "**")

    # Word replacements
    command = command.replace("plus", "+")
    command = command.replace("minus", "-")
    command = command.replace("times", "*")
    command = command.replace("into", "*")
    command = command.replace("over", "/")
    command = command.replace("mod", "%")
    command = command.replace("power", "**")

    # Remove trigger words
    command = command.replace("what is", "")
    command = command.replace("calculate", "")
    command = command.strip()

    print(f"Parsed Expression: {command}")  # For debugging

    # Only allow safe characters
    if not re.match(r'[\d\s\+\-\/\.\(\)\%]+$', command):
        speak("Sorry, I can only calculate basic math expressions.")
        return

    try:
        result = eval(command)
        speak(f"The answer is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        print(f"Calculation error: {e}")
def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = f"C:/Users/vikra/OneDrive/Pictures/pics/{filename}"  # Change this path as needed

    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    speak(f"Screenshot taken and saved as {filename}")
def social_media(command):
    platforms = {
        'facebook': "https://www.facebook.com/",
        'whatsapp': "https://web.whatsapp.com/",
        'discord': "https://discord.com/",
        'instagram': "https://www.instagram.com/",
        'twitter': "https://twitter.com/",
        'linkedin': "https://www.linkedin.com/",
        'youtube': "https://www.youtube.com/"
    }

    for key in platforms:
        if key in command:
            speak(f"Opening your {key}")
            webbrowser.open(platforms[key])
            return

    speak("No social media platform matched your command.")
def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])
def openApp(command):
    command = command.lower()
    app_map = {
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "chrome": "chrome",
        "word": "winword",
        "excel": "excel",
        "powerpoint": "powerpnt",
        "vlc": "vlc",
        "spotify": "spotify",
        # Add more common aliases here if needed
    }

    for app_name in app_map:
        if app_name in command:
            speak(f"Opening {app_name}")
            try:
                os.system(f"start {app_map[app_name]}")
            except:
                speak(f"Could not open {app_name}")
            return

    # If not in predefined map, try to open as-is
    try:
        app_to_open = command.replace("open", "").strip()
        speak(f"Trying to open {app_to_open}")
        os.system(f"start {app_to_open}")
    except Exception as e:
        speak("I couldn't open the application.")
        print(f"Error: {e}")
import pygetwindow as gw
@eel.expose
def closeApp(command):
    command = command.lower()
    app_map = {
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        # Add more mappings here as needed
    }

    if "calculator" in command:
        speak("Closing calculator")
        try:
            window = gw.getWindowsWithTitle('Calculator')[0]
            window.close()
        except IndexError:
            speak("No open calculator window found.")
        return

    app_key = next((key for key in app_map if key in command), None)
    if app_key:
        process_name = app_map[app_key]
        speak(f"Closing {app_key}")
        os.system(f"taskkill /f /im {process_name}")
        return

    # Fallback: try to extract app name and add `.exe`
    try:
        app_to_close = command.replace("close", "").strip().replace(" ", "") + ".exe"
        speak(f"Trying to close {app_to_close}")
        os.system(f"taskkill /f /im {app_to_close}")
    except Exception as e:
        speak("I couldn't close the application.")
        print(f"Error: {e}")
def browsing(command):
    if 'google' in command:
        speak("Boss, what should i search on google..")
        s = command.lower()
        webbrowser.open(f"https://www.google.com/search?q={s}")
    elif 'Youtube' in command:
        speak("Boss, what should i search on youtube..")
        s = command.lower()
        webbrowser.open(f"https://www.youtube.com/results?search_query={s}")

reminders = []

def set_reminder(task, delay_seconds):
    def reminder_action():
        speak(f"Reminder: {task}")
        print(f"Reminder: {task}")

    timer = threading.Timer(delay_seconds, reminder_action)
    timer.start()
    reminders.append((task, time.time() + delay_seconds))
    speak(f"I'll remind you to {task} in {delay_seconds // 60} minutes.")

# Example usage in command handler
def handle_reminder_command(command):
    import re
    match = re.search(r"remind me to (.+?) in (\d+)\s?(seconds|minutes|minute|second)", command)
    if match:
        task = match.group(1)
        time_value = int(match.group(2))
        unit = match.group(3)

        delay = time_value * 60 if "minute" in unit else time_value
        set_reminder(task, delay)
    else:
        speak("Sorry, I didn't understand the reminder.")


def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

import os
import shutil

def manage_files(command):
    if "create a folder named" in command:
        folder_name = command.replace("create a folder named", "").strip()
        try:
            os.makedirs(folder_name)
            speak(f"Folder named {folder_name} has been created.")
        except FileExistsError:
            speak("That folder already exists.")
    elif "delete folder named" in command:
        folder_name = command.replace("delete folder named", "").strip()
        try:
            shutil.rmtree(folder_name)
            speak(f"Folder named {folder_name} has been deleted.")
        except FileNotFoundError:
            speak("That folder does not exist.")
    elif "delete file named" in command:
        file_name = command.replace("delete file named", "").strip()
        try:
            os.remove(file_name)
            speak(f"File named {file_name} has been deleted.")
        except FileNotFoundError:
            speak("That file does not exist.")
import os

def search_file(command):
    filename = command.replace("search for file named", "").strip()
    search_path = "C:/Users/vikra/OneDrive/Desktop/Jarvis/"  # You can change this to a specific directory

    speak(f"Searching for {filename}")
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            full_path = os.path.join(root, filename)
            speak(f"File found at {full_path}")
            print(f"File found: {full_path}")
            return

    speak("Sorry, I could not find the file.")


def read_text_file(command):
    filename = command.replace("read file named", "").strip()
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    try:
        with open(filename, 'r') as file:
            content = file.read()
            speak("Reading the contents of the file")
            print(content)
            speak(content)
    except FileNotFoundError:
        speak("Sorry, I could not find that file.")
    except Exception as e:
        speak("Something went wrong while reading the file.")
        print(f"Error: {e}")

def view_processes():
    speak("Here are some of the running processes:")
    process_list = list(psutil.process_iter(['pid', 'name']))[:10]  # Convert to list before slicing
    for proc in process_list:
        process_info = f"{proc.info['name']} with PID {proc.info['pid']}"
        print(process_info)
        speak(process_info)

def open_task_manager():
    speak("Opening Task Manager")
    os.system("taskmgr")

def close_task_manager():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "Taskmgr.exe" in proc.info['name']:
                os.kill(proc.info['pid'], 9)  # Force kill
                speak("Task Manager has been closed.")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    speak("Task Manager is not running.")

import asyncio
from googletrans import Translator

async def translate_text(command):
    text_to_translate = command.replace("translate", "").strip()
    lang_to = "es"

    translator = Translator()
    translated = await translator.translate(text_to_translate, dest=lang_to)
    
    speak(f"The translation is: {translated.text}")

@eel.expose
def process_command(command):
    
    command = command.lower()
    response = ""

    if "hello" in command:
        response = "Hello! How can I assist you today?"

    elif "time" in command:
        now = datetime.now()
        response = f"The current time is {now.strftime('%I:%M %p')}."

    elif "date" in command:
        today = datetime.date.today()
        response = f"Today's date is {today.strftime('%B %d, %Y')}."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."

    elif "play" in command:
        song = command.replace("play", "").strip()
        pywhatkit.playonyt(song)
        response = f"Playing {song} on YouTube."

    elif "shutdown" in command:
        response = "Shutting down. Goodbye!"
        speak(response)
        eel.display_response(response)
        os._exit(0)
    elif "bye" in command:
        speak("Bye Vikram")
        eel.closeWindow()  # <-- This will call the JS function to close the browser
        time.sleep(1)      # Give it a moment before shutting backend
        sys.exit()
    elif "write a note" in command or "take a note" in command:
         write_note()
    elif "translate" in command:
         asyncio.run(translate_text(command))
    elif ('facebook' in command) or ('discord' in command) or ('whatsapp' in command) or ('instagram' in command) or ('linkedin' in command) or ('youtube' in command) or ('twitter' in command):
         social_media(command)
    elif ("time table" in command) or ("schedule" in command):
         schedule()
    elif ("volume up" in command) or ("increase volume" in command):
         pyautogui.press("volumeup")
         speak("Volume increased")
    elif ("volume down" in command) or ("decrease volume" in command):
         pyautogui.press("volumedown")
         speak("Volume decrease")
    elif ("volume mute" in command) or ("mute the sound" in command):
         pyautogui.press("volumemute")
         speak("Volume muted")
    elif ("volume unmute" in command) or ("unmute the sound" in command):
         pyautogui.press("volumemute")
         speak("Volume unmuted")
    elif ("open calculator" in command) or ("open notepad" in command) or ("open paint" in command) or ("open spotify" in command) or ("open vlc" in command)or ("open powerpoint" in command)or ("open excel" in command)or ("open chrome" in command):
        openApp(command)
    elif ("close calculator" in command) or ("close notepad" in command) or ("close paint" in command)or ("close spotify" in command) or ("close vlc" in command)or ("close powerpoint" in command)or ("close excel" in command)or ("close chrome" in command):
        closeApp(command)
    elif("screenshot" in command):
        take_screenshot()
    elif "calculate" in command or "what is" in command:
         calculate(command)

    
    elif ("what" in command) or ("who" in command) or ("how" in command) or ("hi" in command) or ("thanks" in command) or ("hello" in command):
            padded_sequences = pad_sequences(tokenizer.texts_to_sequences([command]), maxlen=20, truncating='post')
            result = model.predict(padded_sequences)
            tag = label_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                 if i['tag'] == tag:
                     speak(np.random.choice(i['responses']))
    elif ("open google" in command) or ("youtube search " in command):
         browsing(command)
    elif ("system condition" in command) or ("condition of the system" in command):
        speak("checking the system condition")
        condition()
    elif "remind me" in command:
        handle_reminder_command(command)
    elif ("create folder named" in command) or ("delete folder named" in command) :
         manage_files(command)
    elif "search for file named" in command:
        search_file(command)

    elif "read file named" in command:
         read_text_file(command)
    elif "write a note" in command or "take a note" in command:
        write_note()
    elif "show processes" in command or "view processes" in command:
         view_processes()
    elif "open task manager" in command:
        open_task_manager()
    elif "close task manager" in command:
        close_task_manager()

    else:
        response = f"I didn't understand that."

    speak(response)
    eel.display_response(response)
    return response

# Launch the web app in a browser
playAssistantSound(r"C:\Users\vikra\Downloads\jarvis-main\jarvis-main\www\assets\audio\start_sound.mp3")
flag = recoganize.AuthenticateFace()
eel.start("index.html", size=(1000, 700), mode='chrome', block=True)
