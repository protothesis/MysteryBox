# COMPREHENSIVE FEATURE SET

# Mode Green (toggle ON)
    # INITIAL SETUP
        # neopixel ring static on green
        # solo pixel static green
    # CONTINUOUS
        # led blinking randomly
        # button triggers redflare
# Mode blinky (toggle OFF)
    # INITIAL SETUP
        # clear neopixel ring
        # solo pixel random color
    # CONTINUOUS
        # neopixel ring blinking randomly
            # blinking according to blink list
            # blink list changes each cycle
            # ring color changes when toggle changes
        # led blinking consistent
        # solo pixel changes with each cycle


# things that happen at beginning of mode
# things that need to happen continuously during the mode


----

# Design Goal
# keep clean separation between
#     pure functions
#         (ie checking whether the toggle has changed
#             or converting meters to yards ) 
#     side effects
#         update
#             change state
#                 (all the data we're keeping track of - invisible to user)
#         commands
#             causes things to happen

----

# data we're tracking
    # mode

    # color of ring
    # brightness of the ring

    # on/of state of each pixel
