import network
import binascii
import secrets

wlan = network.WLAN() #  network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan() # list with tupples with 6 fields ssid, bssid, channel, RSSI, security, hidden
i=0
networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)

class WIFI():
	def __init__(self, ssid=secrets.SSID, passwd=secrets.PASSWORD):
		self.ssid = ssid
		self.passwd = passwd
	
	@property
	def connect(self):
		wlan = network.WLAN(network.STA_IF)
		wlan.active(True)
		wlan.connect(self.ssid, self.passwd)
		return dict({'isconnected': wlan.isconnected(), 'ifconfig':wlan.ifconfig()})
		
	def scan(self):
		for w in networks:
			i+=1
			print(i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5])

