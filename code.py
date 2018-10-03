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

def generateRandomValue():  # returns a float val between 0 and 1
	#
	return random.random()




### //// COMMAND FUNCTIONS  (use prefix "do" naming convention)
def doPixelsColor(color, brightness = .01):  # fills the CPX ring a color and brightness
    cpx.pixels.brightness = brightness
    cpx.pixels.fill(color)

def doToggleLED():  # toggles the on board LED
	#
	cpx.red_led = not cpx.red_led

def doTogglePixel(index, color):  # 'toggles' an individual CPX pixel
	if cpx.pixels[index] == BLACK:
		cpx.pixels[index] = color
	else:
		cpx.pixels[index] = BLACK
	# print("Pixel %d Toggled" % index)

def doPrintToSerial():  # prints a bunch of state information to serial for TouchDesigner
	'''
		There are occasional instances where there are redundant messages printed.
		This shouldnt cause any issues in Touch Designer...
		but I wonder or worry that its a symptom of some inefficiency or problem in the code
	'''
	print(
		"toggle: %d" % toggle.value, 
		"/",
		"button: %d" % current_button_state,
		"/",
		"flare: %f" % flare_value,
		"/",
		# "LED: %d" % cpx.red_led,
		# "/",
		"neocolor:", neo[0],
		)
	# pass  # to quickly turn off if other testing needs to be done




### //// NEW STATE VARIABLES (standard python underscore separator)
mode = None
pause_duration_LED = .5
previous_time_toggle_LED = currentTime()

redflare = None
flare_value = 0  # generateRandomValue()

current_button_state = button.value

# blinky variables
previous_time_blink = currentTime()
pause_duration_blink = random.uniform(.05,.5)
blink_count = random.randint(3,20)
blinks_per_cycle = 0
blinky_color = BLUE




### //// UPDATE HELPERS
# updates do BOTH - COMMANDS and UPDATES - use cautiously!!

def updateIfItIsTimeToggleLED(new_pause_duration = .25):  # toggles the onboard LED if its time to do so
	global previous_time_toggle_LED
	global pause_duration_LED

	if isItTime(previous_time_toggle_LED, pause_duration_LED):
		doToggleLED() # toggle the LED
		previous_time_toggle_LED = currentTime()
		pause_duration_LED = new_pause_duration

		#doPrintToSerial()

def updateBlinkyCycleSetup():  # preps the CPX ring to blink
	global blinks_per_cycle
	global blink_count

	# initializes the number of blinks, resets the increment tracker, wipes CPX pixels
	blinks_per_cycle = random.randint(3,20)
	blink_count = 0
	doPixelsColor(BLACK)

	# set random solo neopixel color
	neo_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	neo.fill(neo_color)

	doPrintToSerial()
	# print("New Blink Cycle Number: %d \n" % blinks_per_cycle)




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

	# a generic button state check
	old_button_state = current_button_state
	current_button_state = buttonIsDown()
	button_state_has_changed = old_button_state != current_button_state



	# COMMANDS SETUP
	# if we just switched to a new mode, do some initial setup

	if mode_has_changed and mode == "green":  # green setup
		# print("Mode :", mode)
		doPixelsColor(GREEN)
		neo.fill(GREEN)

	elif mode_has_changed and mode == "blinky":  # blinky setup
		#print("Mode :", mode)
		blinky_color = random.choice(COLORS)
		updateBlinkyCycleSetup()
		cpx.stop_tone()

	if mode_has_changed:
		doPrintToSerial()

	# if the button has changed state, do stuff...
	if button_state_has_changed:
		doPrintToSerial()



	# CONTINUOUS UPDATES
	if mode == "green":
		updateIfItIsTimeToggleLED()

		# redflare setup
		if redflare_has_changed and redflare:
			cpx.start_tone(random.randint(250,700))  # sound a random tone

		elif redflare_has_changed and not redflare:
			cpx.stop_tone()  # kill the tone

			# resets CPX ring and solo Neo to green at low brightness
			flare_value = 0
			doPixelsColor(GREEN)
			neo.fill(GREEN)
			neo.brightness = .01

			doPrintToSerial()


		# redflare continuous
		if redflare: 

			# flares CPX ring and solo Neo red at a random brightness
			flare_value = generateRandomValue()
			doPixelsColor(RED, brightness = flare_value)
			neo.fill(RED)
			neo.brightness = flare_value

			doPrintToSerial()


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