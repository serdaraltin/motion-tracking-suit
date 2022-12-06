#!/usr/bin/env python3

import I2C

# sensor data
class Gyro:
    pass

class Magn:
    pass

class Accel:
    pass

class Temp:
    pass


# actual class
class mpu9255:

    __SMPLRT_DIV = 0x19
    __CONFIG = 0x1A         
    __GYRO_CONFIG = 0x1B    
    __ACCEL_CONFIG = 0x1C
    __ACCEL_CONFIG2 = 0x1D

    __ACCEL_XOUT_H = 0x3B
    __ACCEL_YOUT_H = 0x3D
    __ACCEL_ZOUT_H = 0x3F

    __GYRO_XOUT_H = 0x43
    __GYRO_YOUT_H = 0x45
    __GYRO_ZOUT_H = 0x47

    __MAGN_ADDR = 0x0c
    __MAGN_XOUT_L = 0x03
    __MAGN_YOUT_L = 0x05
    __MAGN_ZOUT_L = 0x07

    __TEMP_OUT_H = 0x41

    __PWR_MGMT_1 = 0x6B


    __WHO_AM_I = 0x75	    # identity of the device, 8 bit
    __WHO_AM_I_VAL = 0x73   # identity of mpu9250 is 0x71
                            # identity of mpu9255 is 0x73


    def __init__(self, pi, bus, device):
        self.bus = bus
        self.pi = pi
        self.h = I2C.I2C(pi, bus, device)
        self.h.write_byte(self.__PWR_MGMT_1, 0x00)

        self.h.write_byte(self.__SMPLRT_DIV, 0x07)
        self.h.write_byte(self.__CONFIG, 0b01000000)
        self.h.write_byte(self.__GYRO_CONFIG, 0b00000000)   # 250dps, 
        self.h.write_byte(self.__ACCEL_CONFIG, 0b00000000)  # 2g-scale
        #self.h.write_byte(self.__ACCEL_CONFIG2, 0b00000000) # low pass

        self.gyro = Gyro()
        self.accel = Accel()
        self.magn = Magn()
        self.temp = Temp()

        self.h.write_byte(0x37,0x02)    # enable i2c master bypass
        self.h_magn = I2C.I2C(self.pi, self.bus, self.__MAGN_ADDR)

    def close(self):
        self.h.close()
        self.h_magn.close()

    def who_am_i(self):
        return self.h.readS16B(self.__WHO_AM_I)

    def read_magn(self):
        self.h_magn.write_byte(0x0A, 0x01)
        sleep(0.1)
        self.magn.data = ( self.h_magn.readS16L(self.__MAGN_XOUT_L, 2),
                           self.h_magn.readS16L(self.__MAGN_YOUT_L, 2),
                           self.h_magn.readS16L(self.__MAGN_ZOUT_L, 2) )

    def read_gyro(self):
        self.gyro.data = ( self.h.readS16B(self.__GYRO_XOUT_H, 2),
                           self.h.readS16B(self.__GYRO_YOUT_H, 2),
                           self.h.readS16B(self.__GYRO_ZOUT_H, 2) )

    def read_accel(self):
        self.accel.data = ( self.h.readS16B(self.__ACCEL_XOUT_H, 2),
                            self.h.readS16B(self.__ACCEL_YOUT_H, 2),
                            self.h.readS16B(self.__ACCEL_ZOUT_H, 2) )

    def read_temp(self):
        self.temp.data = self.h.readS16B(self.__TEMP_OUT_H, 2)

if __name__ == '__main__':
    import pigpio
    from time import sleep

    pi = pigpio.pi()
    MPU9255_ADDR = 0x68
    I2C_BUS = 1

    s = mpu9255(pi, I2C_BUS, MPU9255_ADDR)
    if(s.who_am_i() == 0x73):
        print('MPU9255 on board!')
    else:
        print(str(s.who_am_i()) + ', what are you? how do I speak to you?')
        exit()

    loop = True
    dt = 0.25
    while loop == True:
        print('Read?', end=' ')
        read = input()

        for k in range(0, int(read)):
            s.read_gyro()
            s.read_accel()
            s.read_magn()
            s.read_temp()
            print ('Gyro: ' + str(s.gyro.data) + '\t' +
                   'Accel: ' + str(s.accel.data) + '\t' +
                   'Magn: ' + str(s.magn.data) + '\t' +
                   'Temp: ' + str((s.temp.data-25)/+21))
            sleep(dt)

        if(int(read) == 0):
            loop = False

    # cleanup!
    s.close()
    pi.stop()
