import machine
from machine import Pin
import time

analog_value = machine.ADC(28)

leds = [
	Pin(0,Pin.OUT), #R
	Pin(1,Pin.OUT), #G
	Pin(2,Pin.OUT)  #B
	]

last_status = 0

def led_select(num=0):
	global last_status
	if last_status != num:
		last_status = num
		for i in range(len(leds)):
			if i == num:
				leds[i].value(1)
			else:
				leds[i].value(0)

while True:
	reading = analog_value.read_u16()
	print("ADC: ", reading)
	time.sleep_ms(200)
	print(10*"\n")
	
	if reading <= 10000:
		led_select(0)
	elif reading <= 35000:
		led_select(2)
	elif reading <= 55000:
		led_select(1)
	