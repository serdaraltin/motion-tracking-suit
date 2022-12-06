#!/usr/bin/env python3

import I2C
from time import sleep
from ctypes import c_ulong

class bmp180:

    # calibration data (16 bits, MSB first)
    __CAL_AC1 = 0xAA
    __CAL_AC2 = 0xAC
    __CAL_AC3 = 0xAE
    __CAL_AC4 = 0xB0
    __CAL_AC5 = 0xB2
    __CAL_AC6 = 0xB4
    __CAL_B1 =  0xB6
    __CAL_B2 =  0xB8
    __CAL_MB =  0xBA
    __CAL_MC =  0xBC
    __CAL_MD =  0xBE

    # control and output registers
    __CONTROL = 0xF4
    __CONTROL_OUTPUT = 0xF6

    # bmp180 modes
    __MODE_ULTRA_LOW_POWER = 0
    __MODE_STANDARD = 1
    __MODE_HIGHRES =  2
    __MODE_ULTRA_HIGHRES = 3

    """
    Be careful! Insanely high oversampling: for conversion times see manual!
    """
    __MODE = __MODE_ULTRA_HIGHRES    # current mode
    __TEMP_CONV_TIME = 5             # ms (depends on mode)
    __PRES_CONV_TIME = 26            # ms (depends on mode)

    # control register
    __READ_TEMPERATURE = 0x2E
    __READ_PRESSURE = 0x34

    # other
    __MSLP = 101920.0               # mean sea level pressure (~101325.0 Pa)

    def __init__(self, pi, bus, device):
        self.h = I2C.I2C(pi, bus, device)
        self.read_cal_data()

    def read_cal_data(self):
        self.AC1 = self.h.readS16B(self.__CAL_AC1, 2)
        self.AC2 = self.h.readS16B(self.__CAL_AC2, 2)
        self.AC3 = self.h.readS16B(self.__CAL_AC3, 2)
        self.AC4 = self.h.readU16B(self.__CAL_AC4, 2)
        self.AC5 = self.h.readU16B(self.__CAL_AC5, 2)
        self.AC6 = self.h.readU16B(self.__CAL_AC6, 2)
        self.B1 = self.h.readS16B(self.__CAL_B1, 2)
        self.B2 = self.h.readS16B(self.__CAL_B2, 2)
        self.MB = self.h.readS16B(self.__CAL_MB, 2)
        self.MC = self.h.readS16B(self.__CAL_MC, 2)
        self.MD = self.h.readS16B(self.__CAL_MD, 2)

    def print_cal_data(self):
        print('AC1: ' + str(self.AC1))
        print('AC2: ' + str(self.AC2))
        print('AC3: ' + str(self.AC3))
        print('AC4: ' + str(self.AC4))
        print('AC5: ' + str(self.AC5))
        print('AC6: ' + str(self.AC6))
        print('B1: ' + str(self.B1))
        print('B2: ' + str(self.B2))
        print('MB: ' + str(self.MB))
        print('MC: ' + str(self.MC))
        print('MD: ' + str(self.MD))

    def read_uncompensated_temperature_value(self):
        self.h.write_byte(self.__CONTROL, self.__READ_TEMPERATURE)
        sleep(self.__TEMP_CONV_TIME * 10**-3) # sleep until data conv
        self.UT = self.h.readS32B(self.__CONTROL_OUTPUT, 2)

    def calculate_true_temperature(self):
        X1 = ((self.UT - self.AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        self.B5 = X1 + X2;
        T = (self.B5 + 8) >> 4
        return T/10.0

    def read_uncompensated_pressure_value(self):
        self.h.write_byte(self.__CONTROL, self.__READ_PRESSURE | (self.__MODE << 6))
        sleep(self.__PRES_CONV_TIME * 10**-3) # sleep until data conv
        self.UP = self.h.readS32B(self.__CONTROL_OUTPUT, 3) >> (8 - self.__MODE)

    def calculate_true_pressure(self):
        B6 = self.B5 - 4000
        X1 = (self.B2 * ((B6 * B6) >> 12)) >> 11
        X2 = self.AC2 * B6 >> 11
        X3 = X1 + X2
        B3 = (((self.AC1*4+X3) << self.__MODE) + 2) >> 2
        X1 = (self.AC3 * B6) >> 13
        X2 = (self.B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = self.ulong((self.AC4 * self.ulong((X3 + 32768))) >> 15)
        B7 = self.ulong((self.ulong(self.UP) - B3) * (50000 >> self.__MODE))

        if(B7 < 0x80000000):
            p = ((B7 << 1) // B4)
        else:
            p = (B7 // B4) << 1

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2= (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
        return p

    def calculate_altitude(self, p):
        return (288.15/0.0065)*(1.0-((p/self.__MSLP)**(1./5.255)))

    def cleanup(self):
        self.pi.i2c_close(self.i2c_handle)

    def ulong(self, x):
        return c_ulong(x).value

    def close(self):
        self.h.close()


if __name__ == '__main__':
    import pigpio

    BMP180_ADDR = 0x77
    I2C_BUS = 1
    pi = pigpio.pi()

    s = bmp180(pi, I2C_BUS, BMP180_ADDR)
    s.print_cal_data()

    s.read_uncompensated_temperature_value()
    s.read_uncompensated_pressure_value()

    temp = s.calculate_true_temperature()
    p = s.calculate_true_pressure()
    alt = s.calculate_altitude(p)
    print('Temp: ' + str(temp) + ' *C')
    print('Pres: ' + str(p) + ' Pa')
    print('Alt: ' + str(round(alt,2)) + ' m')

    # cleanup!
    s.close()
    pi.stop()
