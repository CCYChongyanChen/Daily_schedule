# import subprocess
import os
from argparse import ArgumentParser

script_name = "daily_schedule.py"
code_folder_path = "C:/Users/67311/OneDrive/Reference/bash_functions/schedule_alarm/"

parser = ArgumentParser()
parser.add_argument("-code", help="show code", action = 'store_true')
parser.add_argument("-code_folder", help="show code_folder", action = 'store_true')
args = parser.parse_args()

if args.code:
    os.startfile(code_folder_path + script_name)
    # subprocess.call('start ' + code_folder_path + script_name, shell=True)
    exit()

if args.code_folder:
    os.startfile(code_folder_path)
    exit()

from datetime import datetime
import keyboard
import time
import subprocess
import win32gui
from datetime import datetime, timedelta
import os
import sys

null = open(os.devnull, 'w')
sys.stdout = null
import pygame
sys.stdout = sys.__stdout__
null.close()


console_handle = win32gui.GetForegroundWindow()
def is_console_focused():
    return win32gui.GetForegroundWindow() == console_handle

def play_mp3(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    now = datetime.now()
    while pygame.mixer.music.get_busy():
        if keyboard.is_pressed('esc') or (datetime.now()-now).total_seconds()>60:
            pygame.mixer.music.stop()

def wait_for_keypress(total_seconds):
    start_time = time.time()

    while total_seconds > time.time() - start_time:
        time.sleep(2)
        if keyboard.is_pressed('esc') and is_console_focused():
            future_time = datetime.now() + timedelta(hours=2)
            future_time_str = future_time.strftime("%H:%M")
            text = "Escape key detected. Sleep for 2 hours. Resume at " + future_time_str
            subprocess.call('echo ' + text, shell=True)
            time.sleep(3600*2)

            text = "The program is resumed"
            subprocess.call('echo ' + text, shell=True)
            return True
    return False

def set_alarm(alarm_time,mode):
    current_time = datetime.now()
    time_difference = alarm_time - current_time

    future_time = datetime.now() + timedelta(seconds=time_difference.total_seconds())
    future_time_str = future_time.strftime("%H:%M")

    text = "Next alarm is set in " + str(time_difference.total_seconds()/60) + " minutes at " + future_time_str
    subprocess.call('echo ' + text, shell=True)

    if time_difference.total_seconds()>0:
        wait_dummy = wait_for_keypress(time_difference.total_seconds())
        if wait_dummy:
            return None
    if mode =="study":
        play_mp3("D:\Study\Functions\\bash_functions\statics\\beautiful_piano.mp3")
    elif mode == "relax":
        play_mp3("D:\Study\Functions\\bash_functions\statics\\summer.mp3")
    elif mode=="backhome":
        play_mp3("D:\Study\Functions\\bash_functions\statics\\backhome.mp3")

def set_alarm_for_new_day():
    print("Start a new day! ")
    while 10<datetime.now().hour < 23:
        if datetime.now().minute < 44:
            alarm_time = datetime.now().replace(minute=44)
            set_alarm(alarm_time,"relax")
        elif datetime.now().minute < 59:
            alarm_time = datetime.now().replace(minute=59)
            if datetime.now().hour == 22:
                set_alarm(alarm_time,"backhome")
            else:
                set_alarm(alarm_time,"study")
        else:
            wait_for_keypress(60)

if __name__=="__main__":
    
    # text = "When an alarm is set, press esc for 5 seconds to put the program to sleep for 2 hours"
    # subprocess.call('echo ' + text, shell=True)
    while True:
        current_time = datetime.now()
        if 10<current_time.hour < 23:
            set_alarm_for_new_day()
        else:
            future_time = datetime.now() + timedelta(hours=1)
            future_time_str = future_time.strftime("%H:%M")
            text = "Outside regular time. Sleep for 1 hour. Resume at " + future_time_str
            subprocess.call('echo ' + text, shell=True)
            time.sleep(3600)
