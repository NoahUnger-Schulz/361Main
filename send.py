import zmq
socket=zmq.Context().socket(zmq.REQ)
socket.connect(f"tcp://localhost:3000")
socket.send_string("This is a message from CS361")
print(socket.recv().decode())