# This is the basic starting functionality of the mystery box prototype

# ---- SETUP !!!

import time
import random

import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_circuitplayground.express import cpx





# ----  DECLARE VARIABLES !!!

# // Set initial CPX pixel brightness
cpx.pixels.brightness = .01

# // setup the external neopixel 
pixpin = board.A3
numpix = 1
neobright = 0.1
neo = neopixel.NeoPixel(pixpin, numpix, brightness=neobright)

# // the toggle switch
toggle = DigitalInOut(board.A6)
toggle.direction = Direction.INPUT
toggle_state = toggle.value 

# // the silver button
button = DigitalInOut(board.A7)
button.direction = Direction.INPUT
button.pull = Pull.UP
button_state = None

# // Color Variables
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# // range of random blinkies
randmin = 3
randmax = 10

# // used to change values elsewhere based on the blinky function finishing
reset = 0
oldreset = None

# // global vars for 'blinkcheck'
blink_speed = 0.5
initial_time = time.monotonic()  # defines starting time



# ----  FUNCTIONS !!!

def buttonpress():  # returns inverse of button press
    return not button.value
    # this is just to fold the code in sublime 

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
    global toggle_state

    if toggle.value != toggle_state:
        print("toggle value :", toggle.value)
        if toggle.value:
            print("ON")
        else:
            print("OFF")
    toggle_state = toggle.value

def blinky():  # blinks the cpx pixels randomly
    print("blinky CALLED")

    # reset pixels and set random brightness
    cpx.pixels.fill(BLACK)  # clear any pixel color
    Bright = random.uniform(.001, .2)
    cpx.pixels.brightness = Bright
    # print("Random Bright:", Bright)
     
    count = 0

    for x in range(random.randint(randmin, randmax)):  # Loop between a random number of times
        pixloc = random.randint(0, 9)  # Choose a random neopixel (pixloc var)
        color = None

        if cpx.pixels[pixloc] == BLUE:  # If the color is blue
            cpx.pixels[pixloc] = BLACK  # set it black
            color = "BLACK"
        else:
            cpx.pixels[pixloc] = BLUE  # otherwise set it blue
            color = "BLUE"
        
        time.sleep(random.uniform(.05, .5))  # short random pause
        print("count:", count, "/", "loc:", pixloc, "/", "color:", color)  # cpx.pixels[pixloc])
        count = count + 1  # increment count

    time.sleep(random.uniform(.05, .5))  # short random pause
    cpx.pixels.brightness = 0  # set brightness to 0
     
    # global keyword allows access to global variables
    global reset
    reset = reset + 1
    print("blinky reset count :", reset)
    print()
    pass
    
def neochange():  # sets random color and brightness for solo neopixel
    neo.brightness = random.random()
    rCol = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    neo.fill(rCol)

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

# var for randomtime
marked_time = time.monotonic()

# def randomtime():
#     random_pause = random.uniform(.5, 2)
#     # global marked_time
#     localtime = current_time

#     if current_time - local_time > random_pause:
#         # local_time = current_time
#         print("random pause :", random_pause)


# ---- DO STUFF !!!

while True:
    current_time = time.monotonic()

    presscheck()
    togglecheck()

    if toggle.value:
        # print("ToggleSwitch ON")

        blinkcheck(blink_speed)
        # cpx.red_led = True

        if buttonpress():
            # print("Pressed")
            cpx.start_tone(random.randint(250,700))
            redflare()
            pass

        else:
            cpx.stop_tone()
            
            cpx.pixels.brightness = .01
            cpx.pixels.fill(GREEN)
            neo.brightness = .1
            neo.fill(GREEN)
            # pass
     
    else:
        # print("ToggleSwitch OFF")
        cpx.red_led = False
        # blinkcheck(.25)

        # neo.fill(BLACK)
        neochange()
        blinky()
        pass
        

    # This little statement checks to see if reset has changed and changes the solo neopixel
    if oldreset is None or reset != oldreset:
        neochange()
    oldreset = reset    

    time.sleep(0.01)
