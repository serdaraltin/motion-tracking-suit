# Registers for MPU-6050
# Programmer: Alfredo Yebra Jr.
# Refer to InvenSenses' Register map here:
# https://www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

# Sample rate divider.
# This 8-bit unsigned register specifies the divider from the gyroscope output rate used to
# generate the Sample Rate for the MPU-60X0.
SMPRT_DIV = const(0x19)

# Configuration.
CONFIG = const(0x1A)

# Power management.
PWR_MGMT_1 = const(0x6B)
PWR_MGMT_2 = const(0x6C)

# Accelerometer
ACCEL_CONFIG = const(0x1C)
ACCEL_XOUT0 = const(0x3B)
ACCEL_YOUT0 = const(0x3D)
ACCEL_ZOUT0 = const(0x3F)

# Temperature
TEMP_OUT0 = const(0x41)

# Gyroscope
GYRO_CONFIG = const(0x1B)
GYRO_XOUT0 = const(0x43)
GYRO_YOUT0 = const(0x45)
GYRO_ZOUT0 = const(0x47)

# Contains the 6-bit I2C address of the MPU-60X0. Defaults to 0x68
WHO_AM_I = const(0x68)

btoi = lambda msb, lsb: (msb << 8 | lsb)\
    if not msb & 0x80 else -(((msb ^ 255) << 8) | (lsb ^ 255) + 1)
