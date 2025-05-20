import zmq
def send_coords(coords):
    socket=zmq.Context().socket(zmq.REQ)
    socket.connect(f"tcp://localhost:3000")
    socket.send_string(str(coords[0])+","+str(coords[1]))
    return (socket.recv().decode())
