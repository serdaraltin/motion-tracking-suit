import network
import binascii
from wireless import secrets


class WIFI():
	def __init__(self, ssid=secrets.SSID, passwd=secrets.PASSWORD):
		self.ssid = ssid
		self.passwd = passwd
		self.wlan = network.WLAN(network.STA_IF)
	
	@property
	def connect(self):
		self.wlan.active(True)
		self.wlan.connect(self.ssid, self.passwd)
		return self.wlan
		
	def scan(self):
		self.wlan = network.WLAN() #  network.WLAN(network.STA_IF)
		self.wlan.active(True)
		self.networks = wlan.scan() # list with tupples with 6 fields ssid, bssid, channel, RSSI, security, hidden
		self.i=0
		self.networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
		
		for w in networks:
			self.i+=1
			print(self.i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5])

