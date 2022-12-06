from machine import I2C, Pin

#configuring i2c
i2c = I2C(scl=Pin(5), sda=Pin(4))

print(i2c.scan())