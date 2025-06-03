import math
import re
#def define(string):
def fakeval(string,blank,vars):
    print(string)
    i=0
    while i<len(string):
        if string[i] in vars.keys():
            val=vars[string[i]]
            string=string[:i]+val+string[i+1:]
            i+=len(val)
        else:
            i+=1
    return string
def eval_parens2(string,functions,vars):
    stack=[]
    i=0
    while i<len(string):
        #print(string)
        if string[i]=="(":
            stack+=[i]
            #print(stack)
        elif string[i]==")":
            #print(stack)
            left=stack.pop(-1)
            expr=string[left:i+1]
            #print(expr) 
            if string[left-1] in functions.keys():
                left-=1
                #print([fakeval(x,{},vars) for x in expr.split(",")])
                mid=str(functions[string[left]]([fakeval(x,{},vars) for x in expr.split(",")]))
            else:
                mid=str((fakeval(expr,{},vars)))
            if not (string[left-1] in "(+-*/%^" or left<1):
                mid="*"+mid
            string=string[:left]+mid+string[i+1:]  
            
            #print(string)
            i+=len(mid)-len(expr) #this -1 could have reprecussions
        i+=1
    print(string)
    return string  


# eval_parens2("(((x+5.1)f(y))%(g(h(x))+1)+(3.3(5)))",
#             {"f":lambda x:x[0]+"^2","g":lambda x:"2*"+x[0],"h":lambda x:x[0]+"+1"}
#             ,{"x":"3","y":"1"})

trigfuncs={"sin":math.sin,"cos":math.cos,"tan":math.tan}
def eval_parens(string,functions,vars):
    stack=[]
    try:
        if string[0] in "+-*/%^,)." or string[-1] in "+-*/%^,(.":
            return "Err"
        if string[0]!="(" or string[-1]!=")":
            #print("add parens")
            string="("+string+")"
            
    except:
        return ""
    i=0
    while i<len(string):
        try:
            if string[i]=="(":
                stack+=[i]
                #print(stack)
            elif string[i]==")":
                #print(stack)
                try:
                    left=stack.pop(-1)
                    expr=string[left:i+1]
                except:
                    return "need ("
                #print(expr)    
                #print(string[left-3:left])
                try:
                    for char in expr[1:-1]:
                        if char in "1234567890"+"(+-*/%^,)."+"ext"+"".join(vars.keys()):
                            pass
                        else:
                            return "undefined"
                except:
                    print("whoops bad check")
                if string[left-3:left] in trigfuncs.keys():
                    #print("trig_func")
                    mid=str(trigfuncs[string[left-3:left]]([eval(x,{},vars) for x in expr[1:-1].split(",")][0]))
                    expr+=string[left-3:left]
                    left-=3
                elif string[left-1] in functions.keys():
                    left-=1
                    mid=str(functions[string[left]]([eval(x,{},vars) for x in expr[1:-1].split(",")]))
                    expr+=string[left]
                else:
                    mid=str((eval(expr,{},vars)))
                if not (string[left-1] in "(+-*/%^," or left<1):
                        mid="*"+mid
                string=string[:left]+mid+string[i+1:]  
                i+=len(mid)-len(expr)
                #print("i,left",i,left)
            elif string[i]=="," and stack==[0]:
                #print("its a point",stack,string,i)
                #print(string[:i]+")","("+string[i+1:])
                return (float(eval_parens(string[:i]+")",functions,vars)),float(eval_parens("("+string[i+1:],functions,vars)))
            i+=1
        except:
            return "Err"
    #print(string)
    if stack!=[]:
        return "need )"
    try:
        return float(string) 
    except:
        return "Not a valid input" 


# print(eval_parens("(2,sin(2))",
#              {"f":lambda x:eval("x*y",{"x":float(x[0])},{"y":float(x[1])}),"g":lambda x:2*float(x[0]),"h":lambda x:float(x[0])+1}
#              ,{"x":3,"y":1}))

#exit()

def define(string,functions,vars):
    try:
        sides=string.split("=")
    except:
        return "Not a string ig???"
    #print(sides)
    if len(sides)<2:
        return (functions,vars)
    if len(sides)>2:
        return "Too many ="
    
    name=sides[0][0]
    if name in list(functions.keys())+list(vars.keys()):
        return name+"var exists"
    if sides[0]==name:
        try:
            val=eval_parens(sides[1],functions,vars)
            func=float(val)
            return (functions,{name:func}|vars)
        except:
            return val 
        #print(functions,{name:func}|vars)
        
    try:
        var_names=sides[0][2:-1].split(",")
        func=lambda x:eval_parens(sides[1],functions,dict(zip(var_names, x))|vars)
        return ({name:func}|functions,vars)
    except:
        return "bad def"
    
# functions={};vars={}
# functions,vars=define("f(x)=x**2",functions,vars)
# functions,vars=define("x=2",functions,vars)
#print(eval_parens("f(x)",functions,vars))

import matplotlib.pyplot as plt
import numpy as np


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
        if define(string,functions,vars)!=(functions,vars):
            outs+=[define(string,functions,vars)]
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
# recursion='x'
# for i in range(10):
#     recursion='f('+recursion+')'
# graphmux(["a=5","f(x)=x**2-2"]+["g(x)="+recursion,"g(x)","(sin(t),t)","f(3)","(1","%1"])
#print(graphmux(["a=1","a*x"],0,1,0.1,0,1,0.1))
