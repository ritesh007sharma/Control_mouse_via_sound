from scipy import fftpack

import sounddevice as sd
import numpy as np
import time
import pyautogui

import queue

q = queue.Queue()

SAMPLE_RATE = 44100

pyautogui.FAILSAFE = False

duration = 10
sd.default.samplerate = SAMPLE_RATE

moves = [0,0,0,0,0]

def movee():
    global moves
    move = sum(moves)/5
    pyautogui.moveTo(pyautogui.position()[0], move)
    #print("moving...")

def print_sound(indata, outdata, frames, time):
    global moves
    height = pyautogui.size()[1]

    
    volume_norm = np.linalg.norm(indata)*10

    x = volume_norm
    in_min = 20
    in_max = 220
    out_max = 0
    out_min = height


    if x < in_min:
        x = in_min
    if x > in_max:
        x = in_max
    move = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    


    
    moves.append(move)
    moves = moves[1:]
    #print(volume_norm, move)
    #print("moving to ", pyautogui.position()[0], -(move))
    
    

stream = sd.InputStream(callback=print_sound, channels=1)
with stream:
    while 1:
        time.sleep(.2)
        movee()

input()
    
