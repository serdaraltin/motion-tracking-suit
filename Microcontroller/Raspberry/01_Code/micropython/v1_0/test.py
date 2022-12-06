import time
import machine
from wireless.wifi import WIFI
from wireless.udp import UDP
from sensors.sensor import SENSOR

#configuring onboard led
led = machine.Pin("LED", machine.Pin.OUT)

#configuring sensor
sensor = SENSOR()

#configuring wifi
wifi =  WIFI()

#configuring udp
udp = UDP()

#connecting wlan
print("SSID: ",wifi.ssid)
wlan = wifi.connect
print("Wlan connecting...")
while wlan.isconnected() != True:
	led.toggle()
	time.sleep(.5)
	led.toggle()
	time.sleep(.5)
	wlan = wifi.connect
print("Wlan connected.")


#sendind sensor data
while True:
	message = "{}".format((sensor.accel,sensor.gyro,sensor.mag,sensor.bmp))
	print("IP: {}\tPort: {}\tMessage: {}".format(udp.ip,udp.port,message))
	udp.send_message(message)
	led.toggle()
	time.sleep(.1)
