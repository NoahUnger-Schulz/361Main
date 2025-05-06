import matplotlib.pyplot as plt
import matplotlib
import os
os.system("xhost +")
import sys
import numpy as np
import math
from pynput import mouse
import time
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller
from copy import deepcopy
import re
Mouse = Controller()



# Disable all key bindings for all axes
#plt.rcParams['keymap.all_axes'] = ''

# Disable navigation key bindings
plt.rcParams['keymap.back'] = ''
plt.rcParams['keymap.forward'] = ''
plt.rcParams['keymap.home'] = ''

# Disable zoom key bindings
plt.rcParams['keymap.zoom'] = ''

# Disable save figure key bindings
plt.rcParams['keymap.save'] = ''

# Disable other key bindings as needed
plt.rcParams['keymap.fullscreen'] = ''
plt.rcParams['keymap.grid'] = ''
plt.rcParams['keymap.yscale'] = ''
plt.rcParams['keymap.xscale'] = ''
plt.rcParams['keymap.pan'] = ''
plt.rcParams['keymap.quit'] = ''
plt.rcParams['keymap.quit_all'] = ''


#event_queue = queue.Queue(maxsize=10)
i=3
s=.01
is_dragging = False
start_position = np.array([0.,0.])
axis_position = np.array([0.,0.])
X=np.array([math.cos(i) for i in range(30)])
Y=np.array([math.sin(i) for i in range(30)])



class Textbox:
    def __init__(self,x,y,text):
        self.coords = [x,y]
        self.text = text
        self.props=dict(boxstyle='round', facecolor='wheat')
        self.bb=None
        self.xbox=None
    def plot(self):
        t=plt.text(self.coords[0], self.coords[1], self.text, fontsize=14,transform=ax.transAxes,
        verticalalignment='top', bbox=self.props)  
        self.bb=t.get_window_extent()
        self.xbox=xbox(self.bb.xmax,self.bb.ymax,self)
        self.xbox.plot()
        return  self.bb
    def in_bounds(self,x,y):
        if self.xbox!=None:
            self.xbox.clicked(x,y)
        if self.bb!=None:
            #print(x,y)
            in_b=(self.bb.xmin+100)-x<10 and -10<(self.bb.xmax+100)-x and (1200-self.bb.ymax)-y<10 and -10<(1200-self.bb.ymin)-y
            return in_b
        else:
            return False
    def clicked(self,x,y):
        return self.in_bounds(x,y)

class xbox(Textbox):
    def __init__(self,x,y,parent):
        self.coords = [x/1000-.13,y/750-0.13]
        self.text = "X"
        self.props=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        self.bb=None
        self.parent=parent
        self.xbox=None
    def plot(self):
        t=plt.text(self.coords[0], self.coords[1], self.text, fontsize=14,transform=ax.transAxes,
        verticalalignment='top', bbox=self.props)  
        self.bb=t.get_window_extent()
        return  self.bb
    def clicked(self,x,y):
        in_b=self.in_bounds(x,y)
        if in_b:
            try:
                Textboxes.remove(self.parent)
            except:
                pass
            try:
                index=Lines.index(self.parent)
                print(index)
                lines=deepcopy(Lines)
                for i in range(index+1,len(lines)):
                    lines[i]=Line(i-1,lines[i].text)
                print(lines)
                lines.pop(index)
                save([s,Textboxes,lines,max(line-1,0)])
            except:
                pass
        return in_b
    
    
class Line(Textbox):
    def __init__(self, index,text):
        super().__init__(0.02,.98-index*.09,text)
        self.index=index
    #plot the cursor
    def clicked(self,x,y):
        in_b=self.in_bounds(x,y)
        if in_b:
            save([s,Textboxes,Lines,self.index])
        return in_b
    def plot(self):
        if self.text[-1]!="|":
            if self.index==line:
                self.text=self.text+"|"
        elif self.index!=line:
            self.text=self.text[:-1]
        super().plot()

    

class button(xbox):
    def __init__(self,x,y, text,func):
        super().__init__(x,y,None)
        self.coords=[x,y]
        self.text=text
        self.func=func
    def clicked(self,x,y):
        in_b=self.in_bounds(x,y)
        if in_b:
            self.func()
        return in_b
class link(button):
    def __init__(self,x,y, text,parent,func):
        super().__init__(x,y, text,func)
        self.parent=parent
        self.props=dict(color="blue")
    def plot(self):
        global Textboxes
        if self.parent in list(map(lambda box:box.text,Textboxes)):
            super().plot()
        else:
            Textboxes.remove(self)
class shortcut(button):
    def __init__(self,x,y, text,boxes):
        super().__init__(x,y,text,None)
        self.boxes=boxes
    def clicked(self,x,y):
        in_b=self.in_bounds(x,y)
        if in_b:
            print("clicked")
            save([s,(Textboxes+self.boxes),Lines,line])
        return in_b


global command
command=False

def save(state,redo=False):
    global redo_states,past_states
    global s,Textboxes,Lines,line
    print(s,Textboxes,Lines,line)
    past_states+=[[deepcopy(s),deepcopy(Textboxes),deepcopy(Lines),deepcopy(line)]]
    print([len(i[2]) for i in past_states])
    s=state[0]
    Textboxes=state[1]
    Lines=state[2]
    line=state[3]
    if not redo:
        redo_states=[]
def redo():
    try:
        save(redo_states.pop(-1),redo=True)
    except:
        pass
def undo():
    global redo_states,past_states
    global s,Textboxes,Lines,line
    try:
        state=past_states.pop(-1)
        print(len(state[2]))
        redo_states+=[[deepcopy(s),deepcopy(Textboxes),deepcopy(Lines),deepcopy(line)]]
        s=state[0]
        Textboxes=state[1]
        Lines=state[2]
        line=state[3]
    except:
        pass




Intro="""
Welcome to  math graphy

Your free offline graphing program

Open a template graph here 

or click x to start graphing 

Save your work in settings

Press ? to get more info about how to graph

"""
Help="""
Plot equations to visualize your mathematics!!

Equations: (soon to be more)
Points: (*,*) where the stars are numbers

Pan around the graph with the mouse or 
use the scaling in settings

Here are some templates that overview 
expression types

Note there are nice ctrl z and y key bindings
so you can easily undo and redo mistakes
"""
Settings=f"""Up and down 
scale the window




These are not 
operational 
yet wait for 
the next 
update :) 

Save
Copy
Open
"""

def upscale():
        global s
        s*=1.1


def downscale():
        global s
        s/=1.1

def Template():
    save([.01,[shortcut(.9,.98,"⚙️",[Textbox(.57,.98,Settings)
                                     ,link(.83,.85,"⬆️",Settings,upscale)
                                     ,link(.83,.75,"⬇️",Settings,downscale)]),
            shortcut(.1,.12,"?",[Textbox(.1,.98,Help),link(.1,.35,"here",Help,None)])
            ,button(.23,.98,"↩️",undo)
            ,button(.3,.98,"↪️",redo)
            ],[Line(0," "),Line(1," (1,1)"),Line(2," (2,2)"),Line(3," (1,2)"),
               Line(4," Here we have graphed 3 points"),
               Line(5," Press the down key to make new line"),
               Line(6," Then type in your own point to plot")],6])

Textboxes=[shortcut(.9,.98,"⚙️",[Textbox(.57,.98,Settings)
                                     ,link(.83,.85,"⬆️",Settings,upscale)
                                     ,link(.83,.75,"⬇️",Settings,downscale)]),
            shortcut(.1,.12,"?",[Textbox(.1,.98,Help),link(.1,.45,"here",Help,Template)])
            ,button(.23,.98,"↩️",undo)
            ,button(.3,.98,"↪️",redo)
            ,Textbox(.1,.98,Intro)
            ,link(.57,.68,"here",Intro,Template)
            ]

Lines=[Line(0," hello"),Line(1," (1,1)")]
line=0
past_states=[]
redo_states=[]



fig, ax = plt.subplots()
def PLOT(x0,y0,s):
    plt.clf()
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='k')  # Add horizontal line at y=0
    plt.axvline(x=0, color='k')  # Add vertical line at x=0
    for equation in Lines:
        if equation.index==line:
            sides=equation.text[1:-1].split(",")
        else:
            sides=equation.text[1:].split(",")
        if len(sides)==2 and sides[0][0]=="("and len(sides[1])>0 and sides[1][-1]==")":
            point=list(map(int,[sides[0][1:],sides[1][:-1]]))
            try:
                plt.scatter(point[0],point[1])
            except:
                print(point)
    plt.axis([s*(-x0-500),s*(-x0+500),s*(y0-500),s*(y0+500)])
    for text in Lines+Textboxes:
        text.plot()
        #print(text.text)
    plt.show(block=False)
    plt.pause(10**-100)
    


def on_press(key):
    global command
    try:
        char=key.char
        if not command:
            lines=deepcopy(Lines)
            lines[line].text=lines[line].text[:-1]+char+"|"
            save([s,Textboxes,lines,line])
        else:
            if (char=="z"):
                print("undoing")
                undo()
            elif(char=="y"):
                redo()
        Mouse.click(Button.right)
    except AttributeError:
        if key==keyboard.Key.ctrl:
            command=True
        if key==keyboard.Key.backspace:
            lines=deepcopy(Lines)
            if len(lines[line].text)>2: 
                lines[line].text=lines[line].text[:-2]+"|"
                save([s,Textboxes,lines,line])
                Mouse.click(Button.right)
            elif (len(Lines)>1):
                try:
                    lines=deepcopy(Lines)
                    for i in range(line+1,len(lines)):
                        lines[i]=Line(i-1,lines[i].text)
                    lines.pop(line)
                    save([s,Textboxes,lines,max(line-1,0)])
                except:
                    pass
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global line, Lines, command
    if key==keyboard.Key.ctrl:
        command=False
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        sys.exit(1)
    if key == keyboard.Key.down or key == keyboard.Key.enter :
        lines=deepcopy(Lines)
        if line>7:
            save([s,Textboxes+[Textbox(.1,.98,"You have made too many lines")],lines,line-1])
        elif line>=len(lines)-1:
            lines+=[Line(line+1," ")]   
            save([s,Textboxes,lines,line+1])
        else:
            save([s,Textboxes,lines,line+1])            
        Mouse.click(Button.right)      
    if key == keyboard.Key.up and line>0:
        line-=1
        
def on_click(x, y, button, pressed):
    global is_dragging, start_position,axis_position
    if pressed and button==mouse.Button.left:
        is_dragging = True
        start_position = np.array([x,y])
        print(f"Drag started at {start_position}")
        for l in Lines+Textboxes:
            print(l.text)
            if l.clicked(x,y):
                print("in bounds")
    if pressed and button==mouse.Button.right:
        (x0,y0)=axis_position
        PLOT(x0,y0,s)
    if not pressed and is_dragging:
        is_dragging = False
        axis_position+=(np.array([x,y])-start_position)
        (x0,y0)=axis_position
        PLOT(x0,y0,s)
        print(f"Drag ended at {(x, y)}")

def on_scroll(x, y, dx, dy):
    global s,i
    i+=1
    if i%2==0:        
        if dy < 0:
            s*=1.1
        else: 
            s/=1.1
        print(s)
        (x0,y0)=axis_position
        PLOT(x0,y0,s)
        

def on_move(x, y):
    if is_dragging:
        global i
        i+=1
        if i%5==0:
            (x0,y0)=axis_position+(np.array([x,y])-start_position)
            PLOT(x0,y0,s)
    else:
        pass
    
keyboard_listener = keyboard.Listener(on_press=on_press,on_release=on_release)
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

try:
    while True:
        time.sleep(0.1)
        if i%5==3:
            Mouse.click(Button.right)
            Mouse.click(Button.right)
        time.sleep(0.5)    
        i+=1        
except KeyboardInterrupt:
    print("Program terminated!")
finally:
    keyboard_listener.stop()
    mouse_listener.stop()
    keyboard_listener.join()
    mouse_listener.join()