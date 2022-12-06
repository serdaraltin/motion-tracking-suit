import time
from wifi import WIFI
from udp import UDP
from sensor import SENSOR


#configuring wifi
wifi =  WIFI()
connection = wifi.connect

#configuring udp
udp = UDP()

#configuring sensor
sensor = SENSOR()


print("Wlan Connection: ",connection.get('isconnected'))


while True:
	udp.send_message("{}\n{}\n{}\n{}".format(sensor.accel,sensor.gyro,sensor.mag,sensor.bmp))
