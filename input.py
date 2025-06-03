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


i=3
s=.01
is_dragging = False
start_position = np.array([0.,0.])
axis_position = np.array([0.,0.])
X=np.array([math.cos(i) for i in range(30)])
Y=np.array([math.sin(i) for i in range(30)])



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



class Textbox:
    def __init__(self,x,y,text):
        self.coords = [x,y]
        self.text = text
        self.props=dict(boxstyle='round', facecolor='wheat')
        self.bb=None
        self.xbox="not none"
    def plot(self):
        t=plt.text(self.coords[0], self.coords[1], self.text, fontsize=14,transform=ax.transAxes,
        verticalalignment='top', bbox=self.props)  
        self.bb=t.get_window_extent()
        if self.xbox!=None:
            self.xbox=xbox(self.bb.xmax,self.bb.ymax,self)
            self.xbox.plot()
        return  self.bb
    def in_bounds(self,x,y):
        if self.xbox!=None:
            self.xbox.clicked(x,y)
        if self.bb!=None:
            in_b=(self.bb.xmin+100)-x<10 and -10<(self.bb.xmax+100)-x and (1200-self.bb.ymax)-y<10 and -10<(1200-self.bb.ymin)-y
            return in_b
        else:
            return False
    def clicked(self,x,y):
        return self.in_bounds(x,y)



class xbox(Textbox):
    def __init__(self,x,y,parent):
        super().__init__(x/1000-.13,y/750-0.13,"X")
        self.parent=parent
        self.xbox=None
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
        super().__init__(0.02,.98-(index)*.09,text)
        self.index=index
    #plot the cursor
    def clicked(self,x,y):
        in_b=self.in_bounds(x,y)
        if in_b:
            save([s,Textboxes,Lines,self.index])
        return in_b
    def plot(self,err):
        if self.text=="":
            lines=deepcopy(Lines)
            lines.remove(self)
            save([s,Textboxes,lines,self.index])
        if self.text[-1]!="|":
            if self.index==line:
                self.text=self.text+"|"
        elif self.index!=line:
            self.text=self.text[:-1]
        temp=self.text
        self.text+=err
        super().plot()
        self.text=temp

class Title(Line):
    def __init__(self,text):
        super().__init__(0,text)
        self.props=dict( facecolor='tan')
        self.xbox=None
    def plot(self,dummy):
        if self.text=="":
            self.text+=" "
        super().plot("")
        self.xbox

    

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





Intro="""
Welcome to  math graphy

Your free offline graphing program

Open a tutorial graph here 

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

Here is a tutorial that overview 
expression types

Note there are nice ctrl z and y key bindings
so you can easily undo and redo mistakes
"""
Settings=f"""Up and down 
scale the window



To save a file edit the title 
and then hit save
To Open a file hit open 
switch to that file's line
and then hit enter

Save
Open
"""


def upscale():
        global s
        s/=1.1

buttons=False

def pan(x,y):
    global axis_position, buttons
    buttons=True
    print(axis_position)
    axis_position+=np.array([x,y])

def downscale():
        global s
        s*=1.1

def value(dic):
    return dic['words']

def listmax(L):
    max=[]
    for elem in L:
        if len(elem)>len(max):
            max=elem
    return max

import zmq
import dill as pickle

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

open_mode=False
user_id="Noah"


Lines=[Title(" Untitled"),Line(0," hello"),Line(1," (1,1)")]
line=0
past_states=[]
redo_states=[]
Textboxes=[]

def upload():
    title=Lines[0].text
    if title[-1]!="|":
        title+='|'
    #dumps current state
    dump=list(map(lambda data:str(pickle.dumps(data), encoding="latin1"),[s,Textboxes,Lines,line]))
    print(dump)
    socket.send_json({
        "user_id": user_id+":"+title,
        "action": "save",
        "words": dump
    })
    #gets lists of titles
    print(socket.recv_string())
    socket.send_json({
    "user_id": user_id,
    "action": "history"
    })
    titles=socket.recv_json()
    if len(titles)>0:
        print(titles)
        titles=listmax(list(map(value,titles)))
        print(titles)
        #adds title if needed
        if not title in titles:
            save_request = {
                "user_id": user_id,
                "action": "save",
                "words": titles+[title]
            }
            socket.send_json(save_request)
            print(titles+[title])
            print(socket.recv_string())
    else:
        save_request = {
                "user_id": user_id,
                "action": "save",
                "words": [title]
            }
        socket.send_json(save_request)
        print(title)
        print(socket.recv_string())

def Open():
    global open_mode
    socket.send_json({
    "user_id": user_id,
    "action": "history"
    })
    print("Open")
    titles=listmax(list(map(value,socket.recv_json())))
    print(titles)
    lines=[]
    for i in range(len(titles)):
        lines+=[Line(i,titles[i])]
    save([s,[],lines,0])
    open_mode=True


def settings():
    save_string="Do you want save your\n progress to the current title?\n\n\n\n"
    open_string="Do you want open a new file?\n\n\n\n"
    return [shortcut(.9,.98,"⚙️",[Textbox(.57,.98,Settings)
            ,link(.83,.85,"+",Settings,upscale),link(.83,.75," -",Settings,downscale)
            ,link(.65,.85,"⬆️",Settings,lambda:pan(0,1000*s)),link(.65,.75,"⬇️",Settings,lambda:pan(0,-1000*s))
            ,link(.57,.8,"⬅️",Settings,lambda:pan(-1000*s,0)),link(.73,.8,"➡️",Settings,lambda:pan(1000*s,0))
            ,link(.57,.32,"Save",Settings,lambda:save([s,(Textboxes+[Textbox(.2,.8,save_string)
            ,link(.3,.5,"Yes",save_string,upload)]),Lines,line]))
            ,link(.57,.24,"Open",Settings,lambda:save([s,(Textboxes+[Textbox(.2,.8,open_string)
            ,link(.3,.5,"Yes",open_string,Open)]),Lines,line]))
            ])]

def BoilerPlate():
    return settings()+[shortcut(.1,.12,"?",[Textbox(.1,.98,Help),link(.1,.45,"here",Help,Tutorial)])
            ,button(.23,.98,"↩️",undo)
            ,button(.3,.98,"↪️",redo)
            ]

def Tutorial():
    save([.01,BoilerPlate(),[Line(0," "),
               Line(1," 1:Press down or enter to make a new line"),
               Line(2," 2:Type in (3,-3) to make a point"),Line(3," 3:Pan with the mouse or in settings")
               ,Line(4," Note if you type the wrong thing you can")
               ,Line(5," use Ctrl-Z or ↩️ to undo or backspace to delete")],5])




Textboxes=BoilerPlate()+[Textbox(.1,.98,Intro)
            ,link(.55,.68,"here",Intro,Tutorial)
            ]






def download(title):
    socket.send_json({
    "user_id": user_id+":"+title,
    "action": "history"
    })
    state=list(map(lambda string:pickle.loads(bytes(string, "latin1")),listmax(list(map(value,socket.recv_json())))))
    print("state:",state)
    save(state)
    print("state saved?")
    global open_mode
    open_mode=False
    Mouse.click(Button.right)

from parser2 import graphmux

fig, ax = plt.subplots()
def PLOT(x0,y0,s):
    global kills
    if kills>1:
        plt.close()
        return
    plt.clf()
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.axhline(y=0, color='k')  # Add horizontal line at y=0
    plt.axvline(x=0, color='k')  # Add vertical line at x=0
    texts=[]
    for equation in Lines:
        if equation.index==line:
            texts+=[equation.text[1:-1]]
        else:
            texts+=[equation.text[1:]]
    vars,realouts=graphmux(texts,-2,2,0.01,-6,6,0.01)
    print(vars)
    errs={}
    for i,err in realouts:
        errs[i]=err
    plt.axis([s*(-x0-500),s*(-x0+500),s*(y0-500),s*(y0+500)])
    for i in range(len(Lines)):
        if i in errs.keys():
            Lines[i].plot("   "+errs[i])
        else:
            Lines[i].plot("")
            
    for text in Textboxes:
        
        text.plot()
        #print(text.text)
    plt.pause(10**-100)
    
kills=0
def unkill():
    global kills
    kills=0
    try:
        Textboxes.remove(unkill_button)
    except:
        pass
    Mouse.click(Button.right)
    Mouse.click(Button.right)
    Mouse.click(Button.right)
unkill_button=button(0,0.5,"You are quitting all your work will\n be lost click here to continue working" \
"\n press Ctrl-Q or escape again to exit",unkill)
def killing():
    global kills
    kills+=1
    if kills>1:
        print("killing")
        plt.close()
        Mouse.click(Button.right)
        keyboard_listener.stop()
        mouse_listener.stop()
        exit(0)
    save([s,Textboxes+[unkill_button],Lines,line])
    Mouse.click(Button.right)
    

def on_press(key):
    global command
    if not open_mode:
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
                elif (char=="q"):
                    killing()
                
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
                elif (len(Lines)>1 and line>0):
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


def warn_about_lines(textboxes,lines):
    if len(lines)>10:
            textboxes+=[Textbox(.1,.98,"Your boxes are going off the screen \n"
                                " this may have negative effects \n" \
                                "on style and perfomance")]
    else:
        try:#doesn't seem to work for removing
            textboxes.remove(Textbox(.1,.98,"Your boxes are going off the screen \n"
                            " this may have negative effects \n" \
                            "on style and perfomance"))
        except:
            pass
    return textboxes

def on_release(key):
    global line, Lines, command
    if key==keyboard.Key.ctrl:
        command=False
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        killing()
    if key == keyboard.Key.enter :
        if not open_mode:
            lines=deepcopy(Lines) 
            textboxes=deepcopy(Textboxes)
            for i in range(line+1,len(lines)):
                lines[i]=Line(i+1,lines[i].text)
            lines=lines[:line+1]+[Line(line+1," ")]+lines[line+1:]   
            textboxes=warn_about_lines(textboxes,lines)    
            save([s,textboxes,lines,line+1])       
            Mouse.click(Button.right)
        else:
            print("downloading")
            download(Lines[line].text)
    if key == keyboard.Key.down:
        lines=deepcopy(Lines)
        textboxes=deepcopy(Textboxes)
        if line>=len(lines)-1 and not open_mode:
            lines+=[Line(line+1," ")]   
        textboxes=warn_about_lines(textboxes,lines)
        save([s,textboxes,lines,line+1])    
        Mouse.click(Button.right)      
    if key == keyboard.Key.up and line>0:
        line-=1
        
def on_click(x, y, button, pressed):
    global is_dragging, start_position,axis_position,buttons
    if not buttons:
        if pressed and button==mouse.Button.left:
            is_dragging = True
            start_position = np.array([x,y])
            print(f"Drag started at {start_position}")
            for l in Lines+Textboxes:
                #print(l.text)
                if l.clicked(x,y):
                    print(l.text)
        if pressed and button==mouse.Button.right:
            (x0,y0)=axis_position
            PLOT(x0,y0,s)
        if not pressed and is_dragging:
            is_dragging = False
            axis_position+=(np.array([x,y])-start_position)
            (x0,y0)=axis_position
            PLOT(x0,y0,s)
            print(f"Drag ended at {(x, y)}")
    else:
        is_dragging = False
        if not pressed:
            print("buttons")
            buttons=False
            (x0,y0)=axis_position
            PLOT(x0,y0,s)
            print(axis_position)

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
    if is_dragging and not buttons:
        global i
        i+=1
        if i%5==0:
            (x0,y0)=axis_position+(np.array([x,y])-start_position)
            PLOT(x0,y0,s)
    else:
        pass

print("If you want to close the program at any time use Ctrl-Q or esc")
print("This program takes control of your mouse to keep the window open are you fine with this? y/n")
if (input()!="y"):
    exit()
print("what's your user id?")
user_id=input() 
Mouse = Controller()
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