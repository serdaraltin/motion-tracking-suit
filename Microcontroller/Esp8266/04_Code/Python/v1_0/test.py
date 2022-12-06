import time
import machine

#configuring onboard led
led = machine.Pin(2, machine.Pin.OUT)

led.value(0)
