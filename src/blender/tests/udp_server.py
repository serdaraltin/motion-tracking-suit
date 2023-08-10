import socket
import time
import json
import bpy
import math
import tkinter

object = bpy.data.objects["sensor_cube"]

ip = "0.0.0.0"
port = 4455

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
soc.bind((ip,port))

print("waiting...")

while True:
    data,addr = soc.recvfrom(1024)
    json_data = json.loads(data)
    roll = json_data["roll"]
    pitch = json_data["pitch"]
    yaw = json_data["yaw"]
    rotation = (roll,pitch,yaw)
    object.rotation_euler = rotation
    print("received:", data, "from", addr)
    bpy.context.view_layer.update()    
