import matplotlib.pyplot as plt
import os
os.system("xhost +")
import numpy as np
import pyautogui
import math
"""from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# ... or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()"""
X,Y=[],[]
for i in range(1000): 
     
    x, y = pyautogui.position()
    X=np.array([math.cos(i) for i in range(30)])
    Y=np.array([math.sin(i) for i in range(30)])
    plt.plot(100*X,100*Y)
    #plt.plot(X*x,Y*y)
    plt.axis([-x-500,-x+500,y-500,y+500])
    plt.show(block=False)
    plt.pause(10**-21)
    plt.clf()