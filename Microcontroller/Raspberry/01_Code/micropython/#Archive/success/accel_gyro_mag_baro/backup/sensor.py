import time
from machine import Pin, I2C
from mpu6050 import MPU6050
from hmc5883l import HMC5883L
from bmp180 import BMP180

class SENSOR():
	def __init__(self, scl=17, sda=16):
		self.scl = scl
		self.sda = sda
		self.i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=400000)
		
		#configuring mpu6050
		self.mpu = MPU6050(self.i2c)
		#configuring hmc5883l
		self.hmc5883l = HMC5883L(scl=self.scl, sda=self.sda)
		#configuring bmp180
		self.bmp180 = BMP180(self.i2c)
		self.bmp180.oversample_sett = 2
		self.bmp180.baseline = 101325
	@property
	def gyro(self):
		return (self.mpu.gyro.x, self.mpu.gyro.y, self.mpu.gyro.z)
	@property
	def accel(self):
		return (self.mpu.accel.x,self.mpu.accel.y,self.mpu.accel.z)
	@property
	def mag(self):
		return self.hmc5883l.read
	@property
	def bmp(self):
		return (self.bmp180.altitude,self.bmp180.pressure,self.bmp180.temperature)


# while True:
#     bmp_temp = bmp180.temperature
#     psure = bmp180.pressure
#     altitude = bmp180.altitude
#     mx, my, mz = hmc5883l.read()
#     
#     ax=round(mpu.accel.x,2)
#     ay=round(mpu.accel.y,2)
#     az=round(mpu.accel.z,2)
#     gx=round(mpu.gyro.x,2)
#     gy=round(mpu.gyro.y,2)
#     gz=round(mpu.gyro.z,2)
#     mx=round(mx,2)
#     my=round(my,2)
#     mz=round(mz,2)
#     mpu_temp=round(mpu.temperature,2)
#     
#     #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        \n\n",end="\r")
#     
#     print(10*"\n")
#     print("Tempature    : mpu:{0}\tbmp:{1}".format(round(mpu_temp,2),round(bmp_temp,2)))
#     print("Barometer    : psure:{0}\talti:{1}".format(round(psure,2),round(altitude,2)))
#     print("Accelometer  : {0}\t{1}\t{2}".format(ax,ay,az))
#     print("Gryoscope    : {0}\t{1}\t{2}".format(gx,gy,gz))
#     print("Magnetometer : {0}\t{1}\t{2}".format(round(mx,2),round(my,2),round(mz,2)))
# 
#     