from machine import Pin
import time

pins = [
	Pin(18, Pin.OUT), #top
	Pin(19, Pin.OUT), #top right
	Pin(13, Pin.OUT), #bottom right
	Pin(16, Pin.OUT), #middle
	Pin(17, Pin.OUT), #top left
	Pin(15, Pin.OUT), #bottom left
	Pin(14, Pin.OUT), #bottom
	Pin(12, Pin.OUT)  #dot
	]


def clear():
	for i in pins:
		i.value(0)
		
nums = [
	[1,1,1,0,1,1,1,0], #0
	[0,1,1,0,0,0,0,0], #1
	[1,1,0,1,0,1,1,0], #2
	[1,1,1,1,0,0,1,0], #3
	[0,1,1,1,1,0,0,0], #4
	[1,0,1,1,1,0,1,0], #5
	[1,0,1,1,1,1,1,0], #6
	[1,1,1,0,0,0,0,0], #7
	[1,1,1,1,1,1,1,0], #8
	[1,1,1,1,1,0,1,0]  #9
	]


def write_num(num=0):
	for j in range(len(pins)):
		pins[j].value(nums[num][j])
