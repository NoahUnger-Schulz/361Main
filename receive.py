import zmq
import time
socket=zmq.Context().socket(zmq.REP)
socket.bind(f"tcp://*:3000")
while True:     
    message=socket.recv()
    print(message.decode())
    socket.send_string("This is a message from CS361")
