# This is the basic starting functionality of the mystery box prototype


### //// IMPORTS
import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx




### //// SETUP THE BOARD

# -- Set initial CPX pixel brightness
cpx.pixels.brightness = .01

# -- setup the external neopixel 
neo = neopixel.NeoPixel(board.A3, 1, brightness = 0.1)

# -- the toggle switch
toggle = DigitalInOut(board.A6)
toggle.direction = Direction.INPUT
prev_toggle_state = toggle.value  # this maybe needs to be moved?

# -- the silver button
button = DigitalInOut(board.A7)
button.direction = Direction.INPUT
button.pull = Pull.UP
button_state = None  # this needs to be moved???




#### //// CONSTANT VARIABLES  (use ALL CAPS naming convention)

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)




### //// PURE FUNCTIONS  (descriptive camel case)

def currentTime():  # returns the current time
	# so this will collapse Sublime Test
	return time.monotonic()

def buttonIsDown():  # returns intuitive button press value
    return not button.value
    # ... this is just to fold the code in SublimeText

def isItTime(previous_time, pause_duration):  # returns if its time to do a thing
	#
	return currentTime() - previous_time > pause_duration




### //// COMMAND FUNCTIONS  (use prefix "do" naming convention)
def doPixelsColor(color, brightness = .01):  # fills the CPX ring a color and brightness
    cpx.pixels.brightness = brightness
    cpx.pixels.fill(color)

def doPixelsOff():  # runs doPixelsColor() to turn all pixels OFF
	# this function COULD be removed, by passing in (BLACK,0) into doPixelsColor() in the loop...
	# but we're keeping it here for conceptual ease
	doPixelsColor(BLACK, 0)

def doToggleLED():  # toggles the on board LED
	#
	cpx.red_led = not cpx.red_led




### //// NEW STATE VARIABLES (standard python underscore separator)
mode = None
pause_duration_LED = .5
previous_time_toggle_LED = currentTime()




### /// UPDATE HELPERS
''' 
	updates do several things
	COMMANDS and UPDATES
	so be careful when writing functions that do both
	cause there could be some shit going down
'''
def updateIfItIsTimeToggleLED(new_pause_duration = .25):  # toggles the onboard LED if its time to do so
	global previous_time_toggle_LED
	global pause_duration_LED

	if isItTime(previous_time_toggle_LED, pause_duration_LED):
		doToggleLED() # toggle the LED
		previous_time_toggle_LED = currentTime()
		pause_duration_LED = new_pause_duration




### //// MAIN LOOP
while True:

	# UPDATES
	# decide current mode and monitor state
	previous_mode = mode
	mode = "green" if toggle.value else "blinky"
	mode_has_changed = previous_mode != mode


	# COMMANDS SETUP
	# if we just switched to a new mode, do some initial setup
	if mode_has_changed and mode == "green":  # green setup
		print(mode)
		doPixelsColor(GREEN)
	elif mode_has_changed and mode == "blinky":  # blinky setup
		print(mode)
		doPixelsOff()


	# CONTINUOUS UPDATES
	if mode == "green":
		updateIfItIsTimeToggleLED()

		if buttonIsDown():
			doPixelsColor(RED, brightness = random.random())  # Flares the Ring RED
		else:
			doPixelsColor(GREEN)

	elif mode == "blinky":
		updateIfItIsTimeToggleLED(new_pause_duration = random.uniform(.005,1))



	time.sleep(0.01)