#!/usr/bin/env python
from types import ORIENTATIONS
from random import choice

def random_orientation():
	"""
	Returns a random orientation numeric.
	"""
	return choice(ORIENTATIONS.values())
