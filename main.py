
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
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
import pygetwindow as gw
import pyautogui
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pythoncom 
from datetime import datetime
import re
import threading
from googletrans import Translator

import eel
# eel.init("www")
# os.system('start msedge.exe --app="http://localhost:5500/index.html"')
# eel.start('index.html', mode=None,host='localhost',block=True)
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)
@eel.expose
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
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
@eel.expose
def command():
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
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        speak("Say that again please")
        return "None"
    return query
@eel.expose
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
from datetime import datetime
@eel.expose
def tell_time_date(command):
    if "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM
        speak(f"The time is {current_time}")
    elif "date" in command:
        current_date = datetime.now().strftime("%A, %d %B %Y")  # Example: Monday, 22 April 2025
        speak(f"Today's date is {current_date}")


import re

import pyautogui
import time
@eel.expose
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

@eel.expose
def calculate(query):
    query = query.lower()

    # Phrase replacements (important to do these FIRST)
    query = query.replace("multiplied by", "*")
    query = query.replace("divided by", "/")
    query = query.replace("power of", "**")
    query = query.replace("to the power of", "**")

    # Word replacements
    query = query.replace("plus", "+")
    query = query.replace("minus", "-")
    query = query.replace("times", "*")
    query = query.replace("into", "*")
    query = query.replace("over", "/")
    query = query.replace("mod", "%")
    query = query.replace("power", "**")

    # Remove trigger words
    query = query.replace("what is", "")
    query = query.replace("calculate", "")
    query = query.strip()

    print(f"Parsed Expression: {query}")  # For debugging

    # Only allow safe characters
    if not re.match(r'[\d\s\+\-\/\.\(\)\%]+$', query):
        speak("Sorry, I can only calculate basic math expressions.")
        return

    try:
        result = eval(query)
        speak(f"The answer is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        print(f"Calculation error: {e}")



@eel.expose
def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = f"C:/Users/vikra/OneDrive/Pictures/pics/{filename}"  # Change this path as needed

    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    speak(f"Screenshot taken and saved as {filename}")
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
@eel.expose
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

@eel.expose
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

# def openApp(command):
#     if "calculator" in command:
#         speak("opening calculator")
#         os.startfile('C:\\Windows\\System32\\calc.exe')
#     elif "notepad" in command:
#         speak("opening notepad")
#         os.system("start notepad")
#     elif "paint" in command:
#         speak("opening paint")
#         try:
#             os.startfile("mspaint")
#         except FileNotFoundError:
#             speak("Couldn't open Paint. Trying an alternative method.")
#             os.system("start mspaint")
@eel.expose
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

        
# def closeApp(command):
#     command = command.lower()
    
#     if "calculator" in command:
#         speak("closing calculator")
#         try:
#             window = gw.getWindowsWithTitle('Calculator')[0]
#             window.close()
#         except IndexError:
#             speak("No open calculator window found.")
    
#     elif "notepad" in command:
#         speak("closing notepad")
#         os.system("taskkill /f /im notepad.exe")

#     elif "paint" in command:
#         speak("closing paint")
#         os.system("taskkill /f /im mspaint.exe")

import os
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

@eel.expose
def browsing(query):
    if 'google' in query:
        speak("Boss, what should i search on google..")
        s = command().lower()
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif 'Youtube' in query:
        speak("Boss, what should i search on youtube..")
        s = command().lower()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

reminders = []
@eel.expose
def set_reminder(task, delay_seconds):
    def reminder_action():
        speak(f"Reminder: {task}")
        print(f"Reminder: {task}")

    timer = threading.Timer(delay_seconds, reminder_action)
    timer.start()
    reminders.append((task, time.time() + delay_seconds))
    speak(f"I'll remind you to {task} in {delay_seconds // 60} minutes.")
@eel.expose
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

@eel.expose
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
@eel.expose
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
@eel.expose
def search_file(query):
    filename = query.replace("search for file named", "").strip()
    search_path = "C:/Users/vikra/OneDrive/Desktop/Jarvis/"  # You can change this to a specific directory

    speak(f"Searching for {filename}")
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            full_path = os.path.join(root, filename)
            speak(f"File found at {full_path}")
            print(f"File found: {full_path}")
            return

    speak("Sorry, I could not find the file.")

@eel.expose
def read_text_file(query):
    filename = query.replace("read file named", "").strip()
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
@eel.expose
def view_processes():
    speak("Here are some of the running processes:")
    process_list = list(psutil.process_iter(['pid', 'name']))[:10]  # Convert to list before slicing
    for proc in process_list:
        process_info = f"{proc.info['name']} with PID {proc.info['pid']}"
        print(process_info)
        speak(process_info)
@eel.expose
def open_task_manager():
    speak("Opening Task Manager")
    os.system("taskmgr")
@eel.expose
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
@eel.expose
async def translate_text(query):
    text_to_translate = query.replace("translate", "").strip()
    lang_to = "es"

    translator = Translator()
    translated = await translator.translate(text_to_translate, dest=lang_to)
    
    speak(f"The translation is: {translated.text}")


eel.start('index.html')
# import yfinance as yf
# from nsetools import Nse
# def get_stock_price(query):
#     nse = Nse()
#     stock_code = query.replace("price of stock", "").strip().upper()

#     try:
#         stock_info = nse.get_quote(stock_code)
#         price = stock_info['lastPrice']
#         speak(f"The current price of {stock_code} is {price} rupees.")
#     except Exception as e:
#         speak("Sorry, I couldn't fetch the stock price.")
#         print(f"Stock price error: {e}")

if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        #query = command().lower()
        query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query) or ('linkedin' in query) or ('youtube' in query) or ('twitter' in query):
            social_media(query)
        elif ("time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("volume unmute" in query) or ("unmute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume unmuted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query) or ("open spotify" in query) or ("open vlc" in query)or ("open powerpoint" in query)or ("open excel" in query)or ("open chrome" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query)or ("close spotify" in query) or ("close vlc" in query)or ("close powerpoint" in query)or ("close excel" in query)or ("close chrome" in query):
            closeApp(query)
        elif("screenshot" in query):
            take_screenshot()
        elif "calculate" in query or "what is" in query:
            calculate(query)

        elif("what time is now" in query ) or (" what is the date" in query):
            tell_time_date(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("youtube search " in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "remind me" in query:
            handle_reminder_command(query)
        elif ("create folder named" in query) or ("delete folder named" in query) :
            manage_files(query)
        elif "search for file named" in query:
            search_file(query)

        elif "read file named" in query:
            read_text_file(query)
        elif "write a note" in query or "take a note" in query:
            write_note()
        elif "show processes" in query or "view processes" in query:
            view_processes()
        elif "open task manager" in query:
            open_task_manager()
        elif "close task manager" in query:
            close_task_manager()
        elif "translate" in query:
            asyncio.run(translate_text(query))
        # elif "price of stock" in query:
        #     get_stock_price(query)




        elif "exit" in query:
            speak("Bye Vikram")
            sys.exit()
# speak("Hello, I'm JARVIS")