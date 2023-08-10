import socket
import time


ip='0.0.0.0'
port=4455

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
s.bind((ip,port))

print('waiting....')
while True:
  data,addr=s.recvfrom(1024)
  s.sendto(data,addr)
  print('received:',data,'from',addr)

