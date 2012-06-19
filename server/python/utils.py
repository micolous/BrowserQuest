#!/usr/bin/env python
from types import ORIENTATIONS
from random import choice

def random_orientation():
	"""
	Returns a random orientation numeric.
	"""
	return choice(ORIENTATIONS.values())

def distance_to(x1, y1, x2, y2):
	"""
	Finds the distance between two points (x1, y1), (x2, y2).
	
	Improvement from JS version:
	JS version simply takes the greater of the two distances and that is
	treated as the total distance.  We use Pythagoras' Theorem to calculate the
	proper distance between the two points.
	
	The in-game effect is that on a 45deg angle between the two points, the
	range returned will be higher.  So things like aggro ranges for mobs will
	be effectively reduced to a circular area, rather than a square.
	
	This is a bug in the JS version of the server which we do not replicate.
	
	Reference: http://en.wikipedia.org/wiki/Pythagorean_theorem
	
	"""
	dist_x = abs(x1 - x2)
	dist_y = abs(y1 - y2)
	
	# Python has a built in "power" operator, **.
	# x to the power of 0.5 is equal to the square root of x.
	# http://www.ucl.ac.uk/Mathematics/geomath/powsnb/pow5.html
	return int(((dist_x ** 2) + (dist_y ** 2)) ** 0.5)
