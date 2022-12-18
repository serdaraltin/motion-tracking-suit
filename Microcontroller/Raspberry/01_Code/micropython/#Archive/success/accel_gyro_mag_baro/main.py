# from machine import Pin, I2C
# from oled import Write, GFX, SSD1306_I2C
# from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
#
# oled = SSD1306_I2C(128, 64, i2c)
# gfx = GFX(128, 64, oled.pixel)
#
# write15 = Write(oled, ubuntu_mono_15)
# write20 = Write(oled, ubuntu_mono_20)
#
# write15.text("Espresso IDE", 0, 0)
# write15.text("micropython-oled", 0, 15)
#
# gfx.line(0, 32, 127, 32, 1)
# gfx.line(0, 33, 127, 33, 1)
#
# write20.text("1234567890", 0, 35)
# write15.text("Ubuntu Mono font", 0, 52)
#
# oled.show()

from bmp180 import BMP180
from hmc5883l import HMC5883L
from mpu6050 import MPU6050
import time

from machine import Pin, I2C
# i2c configure
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)

# configuring mpu6050
mpu = MPU6050(i2c)

# configuring hmc5883l
hmc5883l = HMC5883L(scl=17, sda=16)

# configuring bmp180
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

# configuring oled
# from oled import Write, GFX, SSD1306_I2C
# from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
# oled = SSD1306_I2C(128, 64, i2c)
# write15 = Write(oled, ubuntu_mono_15)
# write20 = Write(oled, ubuntu_mono_20)

while True:
    bmp_temp = bmp180.temperature
    psure = bmp180.pressure
    altitude = bmp180.altitude
    mx, my, mz = hmc5883l.read()

    ax = round(mpu.accel.x, 2)
    ay = round(mpu.accel.y, 2)
    az = round(mpu.accel.z, 2)
    gx = round(mpu.gyro.x, 2)
    gy = round(mpu.gyro.y, 2)
    gz = round(mpu.gyro.z, 2)
    mx = round(mx, 2)
    my = round(my, 2)
    mz = round(mz, 2)
    mpu_temp = round(mpu.temperature, 2)

    #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        \n\n",end="\r")

    print(10*"\n")
    print("Tempature    : mpu:{0}\tbmp:{1}".format(
        round(mpu_temp, 2), round(bmp_temp, 2)))
    print("Barometer    : psure:{0}\talti:{1}".format(
        round(psure, 2), round(altitude, 2)))
    print("Accelometer  : {0}\t{1}\t{2}".format(ax, ay, az))
    print("Gryoscope    : {0}\t{1}\t{2}".format(gx, gy, gz))
    print("Magnetometer : {0}\t{1}\t{2}".format(
        round(mx, 2), round(my, 2), round(mz, 2)))

#     write15.text("{acelX:.2f}|{gyroX:>3.2f}|{magX:.0f}".format(acelX=ax,gyroX=gx,magX=mx),0,0)
#     write15.text("{acelY:.2f}|{gyroY:>3.2f}|{magY:.0f}".format(acelY=ay,gyroY=gy,magY=my),0,15)
#     write15.text("{acelZ:.2f}|{gyroZ:>3.2f}|{magZ:.0f}".format(acelZ=az,gyroZ=gz,magZ=mz),0,30)
#     oled.show()

    time.sleep(0.2)
