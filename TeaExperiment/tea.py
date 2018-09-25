# EXPERIMENTAL EXPERIMENT
# trying to set up something like The Elm Architecture


import time
import random
from collections import namedtuple
from functools import reduce


Msg = namedtuple("Msg", ["description", "value"])
App = namedtuple("App", 
	["model", "update", "subscriptions", "prev_subscriptions", "counter"]
)
Subscription = namedtuple(
	"Subscription", 
	["target", "description", "msg_description"]
)
# Tracker = namedtuple("Tracker", ["description", "target", "msg_creator"])


def check_subscription_change(sub, prev_subscriptions):
	# print("checking " + sub.description)
	prev_value = prev_subscriptions[sub.description]
	if prev_value:
		if prev_value != sub.target.value:
				return True
	return False


def run(initial_model, update, subscriptions):
	app = App(
		model = initial_model,
		update = update,
		subscriptions = subscriptions,
		prev_subscriptions = {
			sub.description: sub.target.value for sub in subscriptions
		},
		counter = 0
	)
	while True:

		# check for events
		has_changed = lambda sub: check_subscription_change(sub, app.prev_subscriptions)
		triggered_subscriptions = filter(has_changed, app.subscriptions)

		# gather msgs
		create_msg = lambda sub: Msg(
			description = sub.msg_description,
			value = sub.target.value
		)
		msgs = map(create_msg, triggered_subscriptions)

		# update the model
		update = lambda acc, msg: app.update(msg, acc)
		new_model = reduce(update, msgs, app.model)
		app = app._replace(model = new_model)

		# do the commands
		print()


		# take a new snapshot of the subscriptions
		app = app._replace(
			prev_subscriptions = {
				sub.description: sub.target.value for sub in subscriptions
			}
		)

		# sleep for a tick
		time.sleep(0.5)



		### DUMMY STUFF

		# update the counter
		app = app._replace(counter = app.counter + 1)

		# mess with inputs to test subs
		if app.counter == 4:
			toggle_switch = lambda sub: (
				sub._replace(target = DummyBoardPin(value = True)) 
					if sub.description == "BIG_SWITCH" 
					else sub
			)
			app = app._replace( 
				subscriptions = list(map(toggle_switch, app.subscriptions))
			)
			# print(app)

		if app.counter == 7:
			push_button = lambda sub: (
				sub._replace(target = DummyBoardPin(value = True)) 
					if sub.description == "SILVER_BUTTON" 
					else sub
			)
			app = app._replace( 
				subscriptions = list(map(push_button, app.subscriptions))
			)
			# print(app)




