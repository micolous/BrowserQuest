#!/usr/bin/env python
from random import randint

class Checkpoint(object):
	def __init__(self, checkpoint_id, x, y, width, height):
		self.checkpoint_id = checkpoint_id
		self.x, self.y = x, y
		self.width, self.height = width, height
	
	def get_random_position(self):
		return (
			self.x + randint(0, self.width),
			self.y + randint(0, self.height)
		)
