# This is the basic starting functionality of the mystery box prototype


# //// SETUP !!!
import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx



# ////  SETUP THE BOARD

# -- Set initial CPX pixel brightness
cpx.pixels.brightness = .01

# -- setup the external neopixel 
pixpin = board.A3
numpix = 1
neobright = 0.1
neo = neopixel.NeoPixel(pixpin, numpix, brightness=neobright)

# -- the toggle switch
toggle = DigitalInOut(board.A6)
toggle.direction = Direction.INPUT

prev_toggle_state = toggle.value 

# -- the silver button
button = DigitalInOut(board.A7)
button.direction = Direction.INPUT
button.pull = Pull.UP
button_state = None




# -- Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# dictionary of colors...
color_swatches = {
    "red": (255, 0, 0),  # red
    "orange": (255, 40, 0),  # orange
    "yellow": (255, 150, 0),  # yellow
    "green": (0, 255, 0),  # green
    "blue": (0, 0, 255),  # blue
    "purple": (180, 0, 255),  # purple
    # "black": (0, 0, 0),  # off
}

# this function is out of order cause of this wacky generator
def cycle_sequence(seq):  # cycles through whatever sequence... 
    while True:
        for elem in seq:
            yield elem

# this used to be a...
# list of colors for use with above dict...
# but now its a 'generator' I believe
# it is being iterated through to select the key value pair from the dict
color_list = cycle_sequence([
	"red",
	"orange",
    "yellow",
    "green",
    "blue",
    "purple",
    # "black",
])

# I'd like to know a way to select the start position of a generator
# this will ALWAYS start on red... 
color_name = next(color_list)  
active_color = None





def blinkcheck(speed):  # non blocking LED blinky
    global initial_time
    # current_time = time.monotonic()  # now set in main loop
    if current_time - initial_time > speed:
        initial_time = current_time
        cpx.red_led = not cpx.red_led


############


# /// NEW PURE FUNCTIONS
def currentTime():
	# so this will collapse Sublime Test
	return time.monotonic()

def buttonIsDown():  # returns inverse of button press
    return not button.value
    # ... this is just to fold the code in SublimeText

def isItTime(previous_time, pause_duration):
	#
	return currentTime() - previous_time > pause_duration


# /// NEW COMMAND FUNCTIONS
def doPixelsColor(color, brightness = .01):
    cpx.pixels.brightness = brightness
    cpx.pixels.fill(color)

def doPixelsOff():
	# this function COULD be removed, by passing in (BLACK,0) into doPixelsColor() in the loop...
	# but we're keeping it here for conceptual ease
	doPixelsColor(BLACK, 0)

def doToggleLED():
	#
	cpx.red_led = not cpx.red_led


# /// NEW STATE VARIABLES
mode = None
pause_duration_LED = .5
previous_time_toggle_LED = currentTime()


# /// NEW UPDATE HELPERS
''' 
	updates do several things
	COMMANDS and UPDATES
	so be careful when writing functions that do both
	cause there could be some shit going down
'''
def updateIfItIsTimeToggleLED(new_pause_duration = .25):
	global previous_time_toggle_LED
	global pause_duration_LED

	if isItTime(previous_time_toggle_LED, pause_duration_LED):
		doToggleLED() # toggle the LED
		previous_time_toggle_LED = currentTime()
		pause_duration_LED = new_pause_duration


# //// DO STUFF !!!
while True:

	# UPDATES
	previous_mode = mode
	mode = "green" if toggle.value else "blinky"
	mode_has_changed = previous_mode != mode


	# COMMANDS SETUP
	if mode_has_changed and mode == "green":
		print(mode)
		doPixelsColor(GREEN)
	elif mode_has_changed and mode == "blinky":
		print(mode)
		doPixelsOff()


	# Continuous UPDATES
	if mode == "green":
		updateIfItIsTimeToggleLED()

		if buttonIsDown():
			doPixelsColor(RED, brightness = random.random())  # Flares the Ring RED
		else:
			doPixelsColor(GREEN)

	elif mode == "blinky":
		updateIfItIsTimeToggleLED(new_pause_duration = random.uniform(.005,1))



	time.sleep(0.01)