import pigpio
from ctypes import c_int16, c_uint16, c_int32, c_uint32

class I2C:

    def __init__(self, pi, bus, device):
        self.pi = pi
        self.device = device
        self.h = self.pi.i2c_open(bus, device)

    def read(self, reg, n, endian = 'B'):
        bytes = []
        for k in range(0,n):
            bytes.append(self.pi.i2c_read_byte_data(self.h, reg+k))

        if(endian == 'L'):
            bytes.reverse()

        res = 0
        for k in range(0,n):
            res = res | (bytes[k] << (8*n-8*(k+1)))

        return res

    # short ints
    def readS16B(self, reg, n=1):
        return c_int16(self.read(reg, n)).value

    def readU16B(self, reg, n=1):
        return c_uint16(self.read(reg, n)).value

    def readS16L(self, reg, n=1):
        return c_int16(self.read(reg, n, 'L')).value

    def readU16L(self, reg, n=1):
        return c_uint16(self.read(reg, n, 'L')).value

    # long ints
    def readS32B(self, reg, n=1):
        return c_int32(self.read(reg, n)).value

    def readU32B(self, reg, n=1):
        return c_uint32(self.read(reg, n)).value

    def readS32L(self, reg, n=1):
        return c_int32(self.read(reg, n, 'L')).value

    def readU32L(self, reg, n=1):
        return c_uint32(self.read(reg, n, 'L')).value

    def write_byte(self, reg, data):
        self.pi.i2c_write_byte_data(self.h, reg, data)

    def close(self):
        self.pi.i2c_close(self.h)
