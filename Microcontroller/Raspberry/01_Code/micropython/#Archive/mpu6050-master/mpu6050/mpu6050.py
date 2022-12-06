from pyb import I2C

from registers import *


class MPU6050(object):
    """I2C communications for MPU-6050."""

    def __init__(self, bus=1, mode=I2C.MASTER, addr=WHO_AM_I):
        """MPU6050 Constructor.

        Initialize an I2C object to communicate with IMU.
        Waking up the device is required since it starts in sleep.

        We will use the conventions of a word in the MPU-6050 is 2 bytes
        or 16 bits.

        :param bus: I2C bus on pyboard.
        :param mode: Either master or slave mode.
        :param addr: Slave address that communicates with master (pyboard).
        """
        self.i2c = I2C(bus)
        self.i2c.init(mode)
        self.addr = addr
        self.accel_data = [0.0] * 3
        self.accel_range = 16.0
        self.accel_rate = 2048.0
        self.gyro_data = [0.0] * 3
        self.gyro_range = 2000.0
        self.gyro_rate = 16.4
        self.block_buffer = bytearray(6)

        # Wake and initialize the accelerometer and gyro to highest sensitivity.
        self.wake()
        self._write_reg(0b00011000, ACCEL_CONFIG)
        self._write_reg(0b00011000, GYRO_CONFIG)

    def wake(self):
        """Wake up MPU-6050.

        Wake MPU-6050 by writing 0x01 to PWR_MGMT_1 register.
        This is required to begin communication.
        """
        self.i2c.mem_write(0x01, self.addr, PWR_MGMT_1)

    def _read_reg(self, buff, src):
        """Read MPU-6050 register.
        
        Use words, half-words etc. as memory buffers to optimize register
        transfers.
        
        :param buff: Buffer for reading data.
        :param src: Source register to read from.
        :return: Register data.
        """
        return self.i2c.mem_read(buff, self.addr, src)

    def _read_byte_block(self, buff, start_reg):
        """Read a chunk of bytes.

        Read 6 consecutive bytes starting fron s

        :param buff: buff: 6 byte buffer for reading data.
        :param start_reg: Source register to START reading from.
        :return: 6 bytes of data.
        """
        pass


    def _write_reg(self, data, dest):
        """Write to MPU-6050 register.

        :param data: Data to be written to destination register.
        :param dest: Destination register to be written to.
        """
        self.i2c.mem_write(data, self.addr, dest)

    def change_sensitivity(self, sensitivity):
        if sensitivity not in (0, 1, 2, 3):
            return
