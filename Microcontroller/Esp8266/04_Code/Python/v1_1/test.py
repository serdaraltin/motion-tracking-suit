import time
import ssd1306
from machine import I2C, Pin
from wireless.wifi import WIFI
from wireless.udp import UDP
from sensors.sensor import SENSOR

#configuring i2c
i2c = I2C(scl=Pin(5), sda=Pin(4))

#configuring onboard led
#led = Pin(2, Pin.OUT)

#configuring sensor
sensor = SENSOR()

#configuring wifi
wifi =  WIFI()

#configuring udp
udp = UDP()

#configuring oled
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
lines= ["","","","",""]

def print_oled(text, index):
	lines[index] = text
	oled.fill(0)
	for i in range(len(lines)):
		oled.text(lines[i], 0, i*15)
	oled.show()

#connecting wlan
print("SSID: ",wifi.ssid)
wlan = wifi.connect

print("Wlan connecting...")
print_oled("Wlan Connecting",0)
print_oled("...",1)

# while wlan.isconnected() != True:
# 	led.value(0)
# 	time.sleep(.5)
# 	led.value(1)
# 	time.sleep(.5)
# 	wlan = wifi.connect
print("Wlan connected.")
print_oled("SSID:{}".format(wifi.ssid),0)
print_oled("IP:{}".format(wlan.ifconfig()[0]),1)
#print_oled("Wlan Connected",2)
print_oled("RIP:{}".format(udp.ip),2)
#sendind sensor data
print_oled("Transmissing...",3)
while True:
	#message = "{}".format((sensor.accel,sensor.gyro,sensor.mag,sensor.bmp))
	message = "{},{},{}".format(sensor.mag[0],sensor.mag[1],sensor.mag[2])
	print("IP: {}\tPort: {}\tMessage: {}".format(udp.ip,udp.port,message))
	udp.send_message(message)
	#time.sleep(.2)
print_oled("Stopped.",3)	
