import dill as pickle
import matplotlib.pyplot as plt
import numpy as np
import zmq

def_socket=zmq.Context().socket(zmq.REQ)
def_socket.connect(f"tcp://localhost:4231")


eval_socket=zmq.Context().socket(zmq.REQ)
eval_socket.connect(f"tcp://localhost:5521")
eval_socket.send_string("This is a message from CS361")
print(eval_socket.recv().decode())


def graphx(func,a,b,dx):
    #print(func(0.1))
    try:
        X=np.arange(a,b,dx)
        Y=[]
        for x in X:
            Y+=[func(x)]
        plt.plot(X,Y)
        return (X,Y)
    except:
        return "your graph failed"
def grapht(func,a,b,dt):
    try:
        T=np.arange(a,b,dt)
        X=[];Y=[]
        for t in T:
            X+=[func(t)[0]]
            Y+=[func(t)[1]]
        plt.plot(X,Y)
        return (X,Y)
    except:
        return "your paramteric graph failed"

def graphexp(val):
    if type(val) is tuple:
        #print("imapoint")
        plt.scatter(val[0],val[1])    
        return (val[0],val[1])
    else:
        val
        return val
#print(eval_parens("(1,2)",{},{}))

def graphmux(strings,x0,xf,dx,t0,tf,dt):
    functions={};vars={}
    outs=[]
    for string in strings:
        def_socket.send_string(list(map(lambda data:str(pickle.dumps(data), encoding="latin1"),
        [string,functions,vars])))
        define=def_socket.recv().decode()
        if define!=(functions,vars):
            outs+=[define]
            try:
                functions,vars=outs[-1]
            except:
                pass
        elif 'x' in string:
            outs+=[graphx(lambda x:float(eval_parens(string,functions,vars|{'x':x})),x0,xf,dx)]
        elif 't' in string:
            outs+=[grapht(lambda t:(eval_parens(string,functions,vars|{'t':t})),t0,tf,dt)]
        else:
            outs+=[graphexp(eval_parens(string,functions,vars))]
    realouts=[]
    for i in range(len(outs)):
        if not (type(outs[i]) is tuple ):
            realouts+=[(i,str(outs[i]))]
    return vars,realouts

import zmq
import time
socket=zmq.Context().socket(zmq.REP)
socket.bind(f"tcp://*:8769")
while True:     
    message=socket.recv()
    print(message.decode())
    socket.send_string("This is a message from CS361")

while True:

    graphmux()