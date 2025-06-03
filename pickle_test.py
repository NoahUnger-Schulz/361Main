import dill as pickle
class obj:
    def __init__(self,func):
        print("hi")
        self.func=func
    def hi():
        print("hi")
A=[1,"10",obj(lambda x:x)]
a=list(map(lambda data:str(pickle.dumps(data), encoding="latin1"),A))
print(a)
print(list(map(lambda string:pickle.loads(bytes(string, "latin1")),a)))

# import pickle

# data = {"example": "data"}
# print(data)
# string_data=str(pickle.dumps(data), encoding="latin1")

# print(string_data)

# # To revert the process
# pickled_data_again = pickle.loads(bytes(string_data, "latin1"))
# data_again = pickle.loads(pickled_data_again)

# print(data_again)