import random
from collections import namedtuple
from tea import (run, App, Msg, Subscription)


# static config
color_names = [
	"red", "yellow", "purple"
]

# define my Model type
Model = namedtuple("Model", [
	"counter", # int
	"mode", # string
	"red_flare", # boolean
	"blink_color" # string
])

# create my initial model
initial_model = Model(
	counter = 0, 
	mode = "BLINKY", 
	red_flare = False,
	blink_color = random.choice(color_names)
)

# implement my update function
def update(msg, model):	
	print("updating! ")
	print(msg)

	if msg.description == "TICK":
		model = model._replace(counter = model.counter + 1)

	elif msg.description == "SILVER_BUTTON_DID_CHANGE":
		button_is_down = msg.value
		# set red_flare True if button is down and mode is GREEN, else False
		new_red_flare = button_is_down and model.mode == "GREEN"
		model = model._replace(red_flare = new_red_flare)

	elif msg.description == "BIG_SWITCH_DID_TOGGLE":
		switch_is_on = msg.value
		if switch_is_on:
			model = model._replace(mode = "GREEN")
		else:
			new_color = random.choice(color_names)
			model = model._replace(mode = "BLINKY", blink_color = new_color)

	return model


def view(model):
	if model.mode == "GREEN":
		if model.red_flare:
			# all red
			# random brightness
		else:
			# all green


# DUMMY INPUTS
DummyBoardPin = namedtuple("DummyBoardPin", ["value"])

subscriptions = [
	Subscription(
		target = DummyBoardPin(value=False), 
		description = "SILVER_BUTTON", 
		msg_description = "SILVER_BUTTON_DID_CHANGE"
	),
	Subscription(
		target = DummyBoardPin(value=False), 
		description = "BIG_SWITCH", 
		msg_description = "BIG_SWITCH_DID_TOGGLE"
	),
]


# run the app
run(
	initial_model = initial_model, 
	update = update,
	subscriptions = subscriptions
)