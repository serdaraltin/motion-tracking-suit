# import time
# from machine import I2C, Pin
# from wireless.wifi import WIFI
# from wireless.udp import UDP
# from sensors.sensor import SENSOR
# 
# #configuring i2c
# i2c = I2C(scl=Pin(5), sda=Pin(4))
# 
# #configuring onboard led
# led = Pin(2, Pin.OUT)
# 
# #configuring sensor
# sensor = SENSOR()
# 
# #configuring wifi
# wifi =  WIFI()
# 
# #configuring udp
# udp = UDP()
# 
# led(0)
# #connecting wlan
# print("SSID: ",wifi.ssid)
# wlan = wifi.connect
# 
# print("Wlan connecting...")
# 
# # while wlan.isconnected() != True:
# # 	led.value(0)
# # 	time.sleep(.5)
# # 	led.value(1)
# # 	time.sleep(.5)
# # 	wlan = wifi.connect
# 
# led(1)
# print("Wlan connected.")
# 
# led_value = True
# while True:
# 	led.value(led_value)
# 	led_value = not led_value
# 	#message = "{}".format((sensor.accel,sensor.gyro,sensor.mag,sensor.bmp))
# 	message = "{},{},{}".format(sensor.mag[0],sensor.mag[1],sensor.mag[2])
# 	print("IP: {}\tPort: {}\tMessage: {}".format(udp.ip,udp.port,message))
# 	udp.send_message(message)
# 	#time.sleep(.2)
# 
# 
import time
import json
from machine import I2C, Pin
from wireless.wifi import WIFI
from wireless.udp import UDP
from sensors.mpu6050_pure import MPU6050

#configuring i2c
i2c = I2C(scl=Pin(5), sda=Pin(4))

#configuring onboard led
led = Pin(2, Pin.OUT)

#configuring mpu
mpu = MPU6050(i2c)

#configuring wifi
wifi =  WIFI()

#configuring udp
udp = UDP()


#connecting wlan
print("SSID: ",wifi.ssid)
wlan = wifi.connect
print("Wlan connecting...")

# while wlan.isconnected() != True:
# 	led.value(0)
# 	time.sleep(.5)
# 	led.value(1)
# 	time.sleep(.5)
# 	wlan = wifi.connect

print("Wlan connected.")
led_value = True
while True:
    led(led_value)
    led_value = not led_value
    message = "{}".format(json.dumps(mpu.get_values))
    print("IP: {}\tPort: {}\tMessage: {}".format(udp.ip,udp.port,message))
    udp.send_message(message)
    #time.sleep(.2)