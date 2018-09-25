# This is the basic starting functionality of the mystery box prototype


# Outline of Sections:
#
# IMPORTS
#   import your packages
#
# SETUP THE BOARD
#   initialize the hardware stuff (only assign values that aren't going to change later.)
#    
# CONSTANT VARIABLES
#   a constant is a value that will never change, but you need to refer to it from multiple places
#
# PURE FUNCTIONS
#   functions that don't have side-effects, they simply compute the answers to your questions
#
# COMMAND FUNCTIONS
#   functions that do have side-effects, e.g. changing a pixel color
#
# STATE VARIABLES
#   the values that change over time and describe the current state of your app, e.g. blinky_color
#
# MAIN LOOP
#   the boss logic. Based on your current state, invoke certain command functions and update the state.



### INPORTS

import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx



### SETUP THE BOARD (use prefix _underscore naming pattern)

# the Circuit Python Express board
_cpx = cpx

# the external Neopixel 
_neo = neopixel.NeoPixel(board.A3, 1, brightness=0.1)

# the toggle switch
_toggle_switch = DigitalInOut(board.A6)
_toggle_switch.direction = Direction.INPUT

# the silver button
_silver_button = DigitalInOut(board.A7)
_silver_button.direction = Direction.INPUT
_silver_button.pull = Pull.UP



### CONSTANT VARIABLES (use ALL CAPS naming pattern)

# -- Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# dictionary of colors...
COLOR_SWATCHES = {
    "red": (255, 0, 0),  # red
    "orange": (255, 40, 0),  # orange
    "yellow": (255, 150, 0),  # yellow
    "green": (0, 255, 0),  # green
    "blue": (0, 0, 255),  # blue
    "purple": (180, 0, 255),  # purple
    # "black": (0, 0, 0),  # off
}

COLOR_NAMES = [
	"red",
	"orange",
    "yellow",
    "green",
    "blue",
    "purple",
    # "black",
]

# how long does the led pause between blinks (when not random)
LED_BLINK_DURATION_STANDARD = 0.25



### PURE FUNCTIONS

def currentTime():
    return time.monotonic()

def generateBlinkyDuration():
    # TODO
    pass

def generateBlinkyPixelSequence():
    # TODO
    pass


### COMMAND FUNCTIONS (use prefix "do" naming pattern)

def doRedflare():  # randomly changes brightness of all pixels
    brightness = random.random()
    print("brightness =", brightness)
    _cpx.pixels.fill(RED)
    _cpx.pixels.brightness = brightness
    _neo.brightness = brightness

def doAllPixelsOff():
    _cpx.pixels.brightness = 0
    _cpx.pixels.fill(BLACK) 

def doAllPixelsSetToColor(color):
    _cpx.pixels.brightness = .01
    _cpx.pixels.fill(color)

def doSoloNeoSetToColor(color):
    # TODO
    pass

def doBlinkLed():
    # TODO
    pass


### STATE VARIABLES (standard python underscore separator)

mode = None # start at None so that the main loop does initial setup
prev_led_blink_time = currentTime()
led_blink_duration = generateLedBlinkDuration()
prev_blinky_blink_time = currentTime()
blinky_duration = generateBlinkyDuration()
blinky_sequence_index = 0
blinky_color_index = 0
solo_neo_color = BLUE # fuck it why not blue


### MAIN LOOP

while True:

    # decide current mode
    previous_mode = mode
    mode = "GREEN" if _toggle_switch.value else "BLINKY"

    # if we just switched to a new mode, do some initial setup
    if mode != previous_mode and mode == "GREEN":
        # setup GREEN mode
        doAllPixelsColor(GREEN)
        led_blink_duration = LED_BLINK_DURATION_STANDARD
        doSoloNeoSetToColor(GREEN)
    elif mode != previous_mode and mode == "BLINKY":
        # setup BLINKY mode
        prev_blinky_blink_time = currentTime()
        blinky_duration = generateBlinkyDuration()
        blinky_sequence_index = 0
        blinky_color_index = (blinky_color_index + 1) % len(COLOR_SWATCHES)
        doAllPixelsOff()
        solo_neo_color = COLOR_SWATCHES[ COLOR_NAMES[solo_neo_color_index] ]
        doSoloNeoSetToColor(solo_neo_color)
    

    # continuous updates and commands for GREEN
    if mode == "GREEN":
        if _silver_button.value:
            # red flare
            doRedflare()
        
        # LED blink
        time_since_prev_led_blink = currentTime() - prev_led_blink_time
        if time_since_prev_led_blink >= led_blink_duration:
            doBlinkLed()
            prev_led_blink_time = currentTime()
            led_blink_duration = generateLedBlinkDuration()

    # continuous updates and commands for BLINKY
    elif mode == "BLINKY":
        # should we blink right now?
        time_since_prev_blink = currentTime() - prev_blinky_blink_time
        should_blink_now = time_since_prev_blink >= blinky_duration
        if should_blink_now:
            # blink the next pixel
            pixel = blinky_pixel_sequence[blinky_sequence_index]
            color_name = COLOR_NAMES[blinky_color_index]
            color = COLOR_SWATCHES[color_name]
            doBlinkPixel(pixel, color)
            # update state
            prev_blinky_blink_time = currentTime()
            blinky_duration = generateBlinkyDuration()
            blinky_sequence_index = blinky_sequence_index + 1
            if blinky_sequence_index >= len(blinky_pixel_sequence):
                # we have reached the end of the sequence, so start over and create a new sequence
                blinky_sequence_index = 0
                blinky_pixel_sequence = generateBlinkyPixelSequence()
                solo_neo_color_index = (solo_neo_color_index + 1) % len(COLOR_NAMES)

        # should the LED blink right now?
        time_since_prev_led_blink = currentTime() - prev_led_blink_time
        if time_since_prev_led_blink >= led_blink_duration:
            # blink it
            doBlinkLed()
            # update state
            prev_led_blink_time = currentTime()


    time.sleep(0.01)


