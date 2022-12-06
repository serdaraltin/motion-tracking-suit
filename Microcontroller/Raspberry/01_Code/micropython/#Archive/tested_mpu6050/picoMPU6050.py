import time
from machine import Pin, I2C
from imu import MPU6050
from hmc5883l import HMC5883L
from bmp180 import BMP180

#i2c configure
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)

#configuring mpu6050
mpu = MPU6050(i2c)

#configuring hmc5883l
hmc5883l = HMC5883L(scl=17, sda=16)

#configuring bmp180
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

while True:
    bmp_temp = bmp180.temperature
    psure = bmp180.pressure
    altitude = bmp180.altitude
    mx, my, mz = hmc5883l.read()
    
    ax=round(mpu.accel.x,2)
    ay=round(mpu.accel.y,2)
    az=round(mpu.accel.z,2)
    gx=round(mpu.gyro.x)
    gy=round(mpu.gyro.y)
    gz=round(mpu.gyro.z)
    mpu_temp=round(mpu.temperature,2)
    
    #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        \n\n",end="\r")
    
    print(10*"\n")
    print("Tempature    : mpu:{0}\tbmp:{1}".format(round(mpu_temp,2),round(bmp_temp,2)))
    print("Barometer    : psure:{0}\talti:{1}".format(round(psure,2),round(altitude,2)))
    print("Accelometer  : {0}\t{1}\t{2}".format(ax,ay,az))
    print("Gryoscope    : {0}\t{1}\t{2}".format(gx,gy,gz))
    print("Magnetometer : {0}\t{1}\t{2}".format(round(mx,2),round(my,2),round(mz,2)))

    
    time.sleep(0.2)
   