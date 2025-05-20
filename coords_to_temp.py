from meteostat import Stations, Hourly
from meteostat.units import fahrenheit
from datetime import datetime
import matplotlib.pyplot as plt


import zmq
import time
socket=zmq.Context().socket(zmq.REP)
socket.bind(f"tcp://*:3000")
while True:     
    message=socket.recv()
    [long,lat]=list(map(float,message.decode().split(",")))
    print(long,lat)
    stations = Stations()
    stations=stations.nearby(long, lat)
    while(True):
        try:
            station = stations.fetch(3)
            date=datetime.today()
            data = Hourly(station, start = datetime(date.year-1,date.month,date.day), end = date)
            data = data.fetch()
            socket.send_string((str(data.iloc[-1]['temp'])+","+str(fahrenheit(data.iloc[-1]['temp']))))
            break
        except:
            pass
