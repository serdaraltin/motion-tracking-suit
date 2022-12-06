import socket
import udp_server

class UDP():
	def __init__(self, ip=udp_server.IP, port=udp_server.PORT):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
	def send_message(self,message):
		self.sock.sendto(message, (self.ip, self.port))