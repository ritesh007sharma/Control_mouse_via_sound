import tkinter as tk
import pyautogui
from threading import Thread
import numpy as np

#import four
#import five

master = tk.Tk()
vw = None

def run(runfile):
  with open(runfile,"r") as rnf:
    exec(rnf.read())

def open1(arg):
    run("five.py")

def open2(arg):
    run("four.py")

def callback():
    #print("click!")
  pass

def resetMouse(event):
    """
    bring the mouse cursor back to the main window and close the top level one
    """
    if event.char == 'r': 
        
        vw.destroy()
        pyautogui.moveTo(master.winfo_x(), master.winfo_y()) 

def voiceWindow():
    
    t1 = Thread(target = open1, args = (10, ))
    t2 = Thread(target = open2, args = (10, ))
    t1.start()
    t2.start()



    
    """
    Create a new window for the voice-mouse option
    """
    global vw 
    vw = tk.Toplevel(master)
    vw.focus_set()
    vw.title("Voice Control")
    
    vw.bind("<Key>", resetMouse)
    vw.geometry("350x200")
    vw.resizable(1, 1)
    
    # button to calibrate voice
    bCal = tk.Button(vw, text="Calibrate", command=callback)
    bCal.pack(fill = tk.BOTH, expand = True)


    
b = tk.Button(master, text="Voice Mode", command=voiceWindow)
b.pack(fill=tk.BOTH, expand=True)

b2 = tk.Button(master, text="Ball Mode", command=callback)
b2.pack(fill=tk.BOTH, expand=True)

master.geometry("500x500")  # You want the size of the app to be 500x500
master.resizable(1, 1)
master.title("Better Mouse")

master.focus_set()
tk.mainloop()
