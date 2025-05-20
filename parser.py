import re
#def define(string):
def eval_parens(string,functions,vars):
    stack=[]
    #print(string)
    i=0
    while i<len(string):
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
                mid=str(functions[string[left]]([eval(x,{},vars) for x in expr.split(",")]))
            else:
                mid=str((eval(expr,{},vars)))
            if not (string[left-1] in "(+-*/%^" or left<1):
                mid="*"+mid
            string=string[:left]+mid+string[i+1:]  
            i+=len(mid)-len(expr)-1 #this -1 could have reprecussions
        i+=1
    return string  


eval_parens("(((x+5.1)f(y))%(g(h(x))+1)+(3.3(5)))",
            {"f":lambda x:eval("x**2",{"x":float(x[0])}),"g":lambda x:2*float(x[0]),"h":lambda x:float(x[0])+1}
            ,{"x":3,"y":1})



def check_type(string):
    [left,right]=string.split("=")
    

def define(string,functions):
    [vars,expr]=string.split(")")
    if vars[0] in list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"):
        name=vars[0]
        vars=vars[0:]
    else:
        return None,None,None
    if not vars[0]=="(":
        return None,None,None
    else:
        vars=vars[0:]
    vars=vars.split(",")
    if not expr[0]=="=":
        return None,None,None
    else:
        expr=expr[0:]
    if name in functions:
        return None,None,None
    functions[name]=[expr,vars]
    return name,vars, functions