# Code for the MysteryBox prototype


### //// IMPORTS
import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx




### //// SETUP THE BOARD

# -- setup the external neopixel 
neo = neopixel.NeoPixel(board.A3, 1, brightness = 0.1)

# -- the toggle switch
toggle = DigitalInOut(board.A6)
toggle.direction = Direction.INPUT

# -- the silver button
button = DigitalInOut(board.A7)
button.direction = Direction.INPUT
button.pull = Pull.UP




#### //// CONSTANT VARIABLES  (use ALL CAPS naming convention)

# Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

COLORS = [
    (255, 0, 0),    # red
    (255, 40, 0),   # orange
    (255, 150, 0),  # yellow
    (0, 255, 0),    # green
    (0, 0, 255),    # blue
    (180, 0, 255),  # purple
]




### //// PURE FUNCTIONS  (descriptive camel case)

def currentTime():  # returns the current time
	#
	return time.monotonic()

def buttonIsDown():  # returns intuitive button press value
	#
    return not button.value
    
def isItTime(previous_time, pause_duration):  # returns if its time to do a thing
	#
	return currentTime() - previous_time > pause_duration

def doGenerateRandomValue():  # returns a float val between 0 and 1
	#
	return random.random()




### //// COMMAND FUNCTIONS  (use prefix "do" naming convention)
def doPixelsColor(color, brightness = .01):  # fills the CPX ring a color and brightness
    cpx.pixels.brightness = brightness
    cpx.pixels.fill(color)

def doToggleLED():  # toggles the on board LED
	#
	cpx.red_led = not cpx.red_led

def doTogglePixel(index, color):
	if cpx.pixels[index] == BLACK:
		cpx.pixels[index] = color
	else:
		cpx.pixels[index] = BLACK
	# print("Pixel %d Toggled" % index)




### //// NEW STATE VARIABLES (standard python underscore separator)
mode = None
pause_duration_LED = .5
previous_time_toggle_LED = currentTime()

redflare = None

# blinky variables
previous_time_blink = currentTime()
pause_duration_blink = random.uniform(.05,.5)
blink_count = random.randint(3,20)
blinks_per_cycle = 0
blinky_color = BLUE

# new experimental variables... need to be approved by Jesse
random_value = doGenerateRandomValue()




### //// UPDATE HELPERS
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

def updateBlinkyCycleSetup():
	global blinks_per_cycle
	global blink_count

	blinks_per_cycle = random.randint(3,20)
	blink_count = 0
	doPixelsColor(BLACK)

	# set random solo neopixel color
	neo_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	neo.fill(neo_color)

	print("New Blink Cycle Number: %d \n" % blinks_per_cycle)




### //// MAIN LOOP
while True:

	# UPDATES
	# decide current mode and monitor state
	previous_mode = mode
	mode = "green" if toggle.value else "blinky"
	mode_has_changed = previous_mode != mode

	# redflare state check
	# possible 'edge case bug thing' - ask jesse
	old_redflare = redflare
	redflare = buttonIsDown()
	redflare_has_changed = old_redflare != redflare




	# COMMANDS SETUP
	# if we just switched to a new mode, do some initial setup
	if mode_has_changed and mode == "green":  # green setup
		print("Mode :", mode)
		doPixelsColor(GREEN)
		neo.fill(GREEN)

	elif mode_has_changed and mode == "blinky":  # blinky setup
		print("Mode :", mode)

		blinky_color = random.choice(COLORS)
		updateBlinkyCycleSetup()

		cpx.stop_tone()




	# CONTINUOUS UPDATES
	if mode == "green":
		updateIfItIsTimeToggleLED()

		# redflare setup
		if redflare_has_changed and redflare:
			cpx.start_tone(random.randint(250,700))
			# print("entering redflare")
			# print("sound on")
		elif redflare_has_changed and not redflare:
			cpx.stop_tone()
			# print("leaving redflare")
			# print("sound off")

			# resets CPX ring and solo Neo to green at low brightness
			doPixelsColor(GREEN)
			neo.fill(GREEN)
			neo.brightness = .01

		# redflare continuous
		if redflare:  # buttonIsDown():
			# flares CPX ring and solo Neo red at a random brightness
			random_value = doGenerateRandomValue()
			doPixelsColor(RED, brightness = random_value)
			neo.fill(RED)
			neo.brightness = random_value



	elif mode == "blinky":
		updateIfItIsTimeToggleLED(new_pause_duration = random.uniform(.005,1))

		# cycle setup
		if blink_count >= blinks_per_cycle:  # if we should refresh
			updateBlinkyCycleSetup()

		# continuous
		if isItTime(previous_time_blink, pause_duration_blink):  # random blink_duration
			# print("previous time:", previous_time_blink, "pause duration:", pause_duration_blink)

			pixel_index = random.randint(0, 9)  # pick a random pixel
			doTogglePixel(pixel_index, blinky_color)  # and toggle it

			pause_duration_blink = random.uniform(.05,.5)  # pick new blink_duration
			previous_time_blink = currentTime()
			blink_count += 1  # increment - blink_count
			
			
	time.sleep(0.01)