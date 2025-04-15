import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import math
X,Y=[],[]
for i in range(100):  
    x, y = pyautogui.position()
    X=np.array([math.cos(i) for i in range(30)])
    Y=np.array([math.sin(i) for i in range(30)])
    plt.plot(100*X,100*Y)
    plt.plot(X*x,Y*y)
    plt.show(block=False)
    plt.pause(10**-21)
    plt.clf()