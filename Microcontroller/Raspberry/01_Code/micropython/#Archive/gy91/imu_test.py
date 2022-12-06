from machine import I2C, Pin
import time
from mpu6050 import *

id=0
i2c = I2C(id=id, scl=Pin(1), sda=Pin(0),freq=200000)

# mpu9250 = MPU9250(i2c)
# bmp280 = BMP280(i2c)
# bmp280.use_case(BMP280_CASE_INDOOR)
# 
# # print("MPU9250 id: " + hex(sensor.whoami))
# 
# 
# while True:
#     print(bmp280.pressure," ",
# 		  bmp280.pressure/100000," ",
# 		  bmp280.temperature/133.3224, " ",
# 		  bmp280.temperature," ",
# 		  mpu9250.acceleration,"",
# 		  mpu9250.gyro ," ",
# 		  mpu9250.magnetic ," ",
# 		  mpu9250.temperature)
#     time.sleep_ms(1000)

print(i2c.scan())