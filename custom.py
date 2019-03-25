from __future__ import print_function
from __future__ import division

import platform
import config
import socket
import time
import math as m

_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

num_led = 120

j = 0
data = []

r = 0
b=0
g=0

    # Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Define rainbow cycle function to do a cycle of all hues.
while True:
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(num_led):
            # tricky math! we use each pixel as a fraction of the full 96-color wheel
            # (thats the i / strip.numPixels() part)
            # Then add in j which makes the colors go around per pixel
            # the % 96 is to make the wheel cycle around
            data1 = (r,g, b)
            #data1 = wheel(((i * 256 // num_led) + j) % 256) 
            data.append(i)
            data.append(data1[0])
            data.append(data1[1])
            data.append(data1[2])
            print(data)
        data = bytes(data)
        _sock.sendto(data, (config.UDP_IP, config.UDP_PORT))
        _sock2.sendto(data, (config.UDP2_IP, config.UDP_PORT))
        _sock3.sendto(data, (config.UDP3_IP, config.UDP_PORT))
        time.sleep(0.5)
        data = []

   





while True:
    j = 0
    data = []
    for p in range(60):
        data.append(p)
        data.append(round(5*(1+(m.sin(p)))))
        data.append(120)
        data.append(j)
        j +=4
    print(data)
    data = bytes(data)
    _sock.sendto(data, (config.UDP_IP, config.UDP_PORT))
    _sock2.sendto(data, (config.UDP2_IP, config.UDP_PORT))
    _sock3.sendto(data, (config.UDP3_IP, config.UDP_PORT))
    time.sleep(0.5)

