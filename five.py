import pyaudio
import math
import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import struct


def rms( data ):
    count = len(data)/2
    form = "%dh"%(count)
    shorts = struct.unpack( form, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

np.set_printoptions(suppress=True) 

CHUNK = 4096
RATE = 44100

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

def mapp(x, in_min, in_max, out_min, out_max):
    if x < in_min:
        x = in_min
    if x > in_max:
        x = in_max
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


for i in range(10000): #to it a few times just to see
    width = pyautogui.size()[0]
    
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = data * np.hanning(len(data)) # smooth the FFT by windowing data
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1

    move = mapp(freqPeak, 400, 700, 0, width)
    pyautogui.moveTo(move, pyautogui.position()[1])

    samples = np.fromstring(data)
    
   
    volume = np.sum(samples**2)/len(samples)
    decibel = 20 * math.log(volume, 10)
    #print("Volume", decibel)
    

stream.stop_stream()
stream.close()
p.terminate()
