# This is the basic starting functionality of the mystery box prototype


# //// SETUP !!!
import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx



# ////  DECLARE VARIABLES !!!

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

# -- range of random blinkies
randmin = 3
randmax = 10

# -- used to change values elsewhere based on the blinky function finishing
reset = 0
oldreset = None

# -- global vars for led blink timing
blink_speed = 0.5
initial_time = time.monotonic()  # defines starting time for blinkcheck()
blinky_time = time.monotonic()  # set a time comparator for blinky()

# -- global vars for CPX pixel blinking
blinkyNew_time = time.monotonic()  # set a time comparator for blinkyNew()
blinklist_index = 0  # current blink index
random_pause = random.uniform(.05, .5)  # current pause duration


# ////  FUNCTIONS !!!
def buttonpress():  # returns inverse of button press
    return not button.value
    # ... this is just to fold the code in SublimeText

def presscheck():  # checks and sets the state of the button
    global button_state
    if not buttonpress() and button_state is None:
        button_state = "pressed"
    if buttonpress() and button_state == "pressed":
        print()
        print("Button Pressed")
        # randomtime()
        # neochange()  # change solo neo pix when loop can be broken!
        button_state = None   

def togglecheck():  # checks and sets the state of the toggle
    # print("toggle checked")
    global prev_toggle_state
    global color_name

    # if toggle.value != prev_toggle_state:
    #     # return True
    #     print("toggle value :", toggle.value)
    #     if toggle.value:
    #         print("ON")
    #         color_name = next(color_list)  # changes color of blinkers when toggle flips
    #     else:
    #         print("OFF")
    #         clearPixels()
    #         ''' 
    #             NOTE!!!
    #             I'd like this to not be in the toggle check function
    #             but have it called elsewhere, but i cant seem to make it happen
    #         '''
    #     # return toggle.value  # this gives unexpected behavior
    # else:
    # 	pass
    # prev_toggle_state = toggle.value

    return prev_toggle_state != toggle.value

def blinklist():  # generate a pixel order list to be used as a nonblocking alternative to blinky()
    pixelcount = random.randint(randmin, randmax) # pick a num of pixels to fuck with
    pix_order_list = []

    for x in range(pixelcount):
    	pix_order_list.append(random.randint(0, 9))
    	# pixloc = random.randint(0, 9)
    #  print(pix_order_list)
    return pix_order_list   # return the value of the list!

blink_list = blinklist()

def blinkyNew():  # WIP for the non blocking blinker generator... 
    # print("\n     blinkyNew() CALLED")
    global active_color
    global color_name

    global blinkyNew_time
    global random_pause

    global blink_list
    global blinklist_index

    active_color = color_swatches[color_name]

    # PSEUDO CODE NOTES!!!
        # if time to do something
            # toggle appropriate light
            # increment current blink index
            # change pause to new random duration
            # if were at the end of list (remember index starts at 0, check length, etc)
                # generate new list
                # set blink index to 0

    if current_time - blinkyNew_time > random_pause:
        blinkyNew_time = current_time 

        if cpx.pixels[blink_list[blinklist_index]] == active_color:  # If the color is the active color
            cpx.pixels[blink_list[blinklist_index]] = BLACK  # set it black
            color = "OFF"
        else:
            cpx.pixels[blink_list[blinklist_index]] = active_color  # otherwise set it to the active color
            color = color_name 

        print(
        # "blink_list \n"
        "index:", blinklist_index, "/", 
        "value:", blink_list[blinklist_index], "/", 
        "color:", color, "/",
        "pause:", random_pause
        )

        blinklist_index += 1

        random_pause = random.uniform(.05, .5)  # current pause duration

        if blinklist_index >= len(blink_list):  # if we're at the end of the list
            blink_list = blinklist()  # generate a new list

            print()
            print("blink_list:", blink_list)

            blinklist_index = 0  # reset the index

            neochange()  # change the solo neopixel
            clearPixels()  # clear the CPX pixels

    else:
        pass

def blinky():  # blinks the cpx pixels randomly
    print("\n    blinky() CALLED")
    print("start loop actual time:", time.monotonic())  # current_time)

    # global keyword allows access to global variables
    global blinky_time
    global active_color
    global color_name
    global reset

    # reset pixels and set random brightness
    cpx.pixels.fill(BLACK)  # clear any pixel color
    Bright = random.uniform(.001, .2)
    cpx.pixels.brightness = Bright

    # this is now calling a generator
    # color_name = next(color_list)  # changes color after each blinky loop
    active_color = color_swatches[color_name]
     
    pixelcount = random.randint(randmin, randmax) # pick a num of pixels to fuck with
    count = 0  # for counting through the iteration loop (mostly for debugging)

    for x in range(pixelcount):  # range(50):  # Loop between a random number of times
        pixloc = random.randint(0, 9)  # Choose a random neopixel (pixloc var)
        random_pause = random.uniform(.05, .5)  # for trying to build non blocking pause
    	loop_time = time.monotonic()

        # if loop_time - blinky_time > random_pause:
        # 	blinky_time = loop_time
        # 	print("pause:", random_pause)
	    	# this time check within the loop is basically never going to fire, or only fire once...
	    	# I need to figure out another solution...

        if cpx.pixels[pixloc] == active_color:  # If the color is the active color
            cpx.pixels[pixloc] = BLACK  # set it black
            color = "OFF"
        else:
            cpx.pixels[pixloc] = active_color  # otherwise set it to the active color
            color = color_name  

        time.sleep(random.uniform(.05, .5))  # short random pause

        print(
        "count:", count, "/", 
        "loc:", pixloc, "/", 
        "color:", color, "/", 
        "looptime:", loop_time
        )

        # print("random pause:", random_pause)
        # print("blinky time:", blinky_time)
        # print("range:", count, "current time", current_time)

        count = count + 1  # increment count
    
    print("-- end loop actual time:", time.monotonic())

    random_pause = random.uniform(.05, .5)  # for trying to build non blocking pause
    time.sleep(random_pause)  # short random pause
    print("-- post pause:", random_pause)

    cpx.pixels.brightness = 0  # set brightness to 0
    reset = reset + 1

    print("-- blinky times reset :", reset, "\n")
    pass
 
def neochange():  # sets random color and brightness for solo neopixel
    neo.brightness = random.random()
    rCol = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    neo.fill(rCol)

def clearPixels():  # reset CPX pixels to OFF and set random brightness
    cpx.pixels.fill(BLACK)  # clear any pixel color
    Bright = random.uniform(.001, .2)
    cpx.pixels.brightness = Bright
 
def inputReady():  # resets CPX pixels to standard green
    cpx.pixels.brightness = .01
    cpx.pixels.fill(GREEN)
    neo.brightness = .1
    neo.fill(GREEN)

def redflare():  # randomly changes brightness of all pixels
    Bright = random.random()
    print("Bright =", Bright)
    cpx.pixels.fill(RED)
    cpx.pixels.brightness = Bright
    neo.brightness = Bright
    pass   

def blinkcheck(speed):  # non blocking LED blinky
    # print("blinkcheck FIRED!")
    global initial_time
    # current_time = time.monotonic()  # now set in main loop
    if current_time - initial_time > speed:
        initial_time = current_time
        cpx.red_led = not cpx.red_led

neochange()




# /// NEW setup declarations
def doPixelsOff():
    cpx.pixels.brightness = 0
    cpx.pixels.fill(BLACK) 

def doModeSetup():
    if mode == "green":
        cpx.pixels.brightness = .01
        cpx.pixels.fill(GREEN)
    else:
        doPixelsOff()

mode = "green" if toggle.value else "blinky"
doModeSetup()


# //// DO STUFF !!!
while True:
    # print(mode)

    # UPDATES
    current_time = time.monotonic()

    previous_mode = mode
    mode = "green" if toggle.value else "blinky"
    mode_has_changed = previous_mode != mode


    # COMMANDS
    if mode_has_changed:
        print(mode)
        doModeSetup()

    time.sleep(0.01)



















    # /// OLD LOOP FOR REFERENCE
    # current_time = time.monotonic()

    # if togglecheck():
    #     if toggle.value:
    #         # change the color
    #         print("it turned on")
    #     else:
    #         print("it turned OFF")
    #         # clear pixels


    # if toggle.value:  # if toggle switch is ON
    #     blinkcheck(random.uniform(.01, 1)) 
    #     if buttonpress():
    #         cpx.start_tone(random.randint(250,700))
    #         redflare()
    #         pass
    #     else:
    #         cpx.stop_tone()
    #         inputReady()
    # else:  # else toggle switch is OFF
    #     blinkcheck(blink_speed)
    #     blinkyNew()

    # prev_toggle_state = toggle.value  # updates the toggle state for next pass
    # time.sleep(0.01)
