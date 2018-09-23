# trying to set up something like The Elm Architecture


import time
from collections import namedtuple
from functools import map, reduce


Msg = namedtuple("Msg", ["description", "payload"])
App = namedtuple("App", ["initial_model", "update", "trackers"])
Sub = namedtuple("Tracker", ["description", "target", "msg_creator"])

def run(app):
	model = app.initial_model
	tracked_values = snapshot(app.trackers)
	while True:

		# check for events
		has_changed = lambda t: t.target.value != tracked_values[t.description]
		triggered_trackers = filter(has_changed, app.trackers)

		# gather msgs
		create_msg = lambda tracker: tracker.create_msg()
		msgs = map(create_msg, triggered_trackers)

		# update the model
		update = lambda acc, msg: app.update(msg, acc)
		model = reduce(update, msgs, model)

		# do the commands
		print(model)

		# sleep for a tick
		time.sleep(0.1)


# PACKAGE USER

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
	if msg.description == "TICK":
		model = model._replace(counter = model.counter + 1)

	elif msg.description == "TOGGLE_FLIPPED_ON":
		model = model._replace(mode = "GREEN")

	elif msg.description == "TOGGLE_FLIPPED_OFF":
		model = model._replace(
			mode = "BLINKY",
			blink_color = random.choice(color_names)
		)

	elif msg.description == "SILVER_BUTTON_DOWN":
		if model.mode == "BLINKY":
			model = model._replace(red_flare = True)

	elif msg.description == "SILVER_BUTTON_UP":
		model = model._replace(red_flare = False)

	return model


def trackers(model):
	return [
		Tracker(
			description = "SILVER_BUTTON",
			target = silver_button_state,
			msg_creator = lambda 
		)
	]
)

# run the app
app = App(
	initial_model = initial_model, 
	update = update, 
	trackers = trackers(initial_model)
)
run(app)

