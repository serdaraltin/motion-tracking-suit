from machine import I2C, Pin
import mpu6050
i2c = I2C(id=0, scl=Pin(17), sda=Pin(16))
accelerometer = mpu6050.accel(i2c)
accelerometer.get_values()
{'GyZ': -235, 'GyY': 296, 'GyX': 16, 'Tmp': 26.64764, 'AcZ': -1552, 'AcY': -412, 'AcX': 16892}