#!/usr/bin/env python

ORIENTATIONS = dict(
	UP = 1,
	DOWN = 2,
	LEFT = 3,
	RIGHT = 4
)

def get_orientation_as_string(orientation):
	if orientation == ORIENTATIONS['UP']:
		return 'up'
	elif orientation == ORIENTATIONS['DOWN']:
		return 'down'
	elif orientation == ORIENTATIONS['LEFT']:
		return 'left'
	elif orientation == ORIENTATIONS['RIGHT']:
		return 'right'
	else:
		raise ValueError, "Orientation numeric is invalid."
