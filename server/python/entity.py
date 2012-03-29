#!/usr/bin/env python
import message
from random import randint

class Entity(object):
	"""
	A basic Entity object in the game.
	"""
	def __init__(self, entity_id, entity_type, kind, x, y):
		# change in python port: id and type are reserved keywords
		self.entity_id = entity_id
		self.entity_type = entity_type
		self.kind = kind
		self.x = x
		self.y = y
	
	def get_state(self):
		"""
		Returns the state of the Entity.  This is a list of values, in the order id, kind, x, y.
		"""
		return [
			self.entity_id,
			self.kind,
			self.x,
			self.y
		]
	
	def spawn(self):
		"""
		Returns a Message to spawn an entity on a client connection.
		"""
		return message.SpawnMessage(self)
	
	def despawn(self):
		"""
		Returns a Message to despawn an entity on a client connection.
		"""
		return message.DespawnMessage(self)
	
	def set_position(self, x, y):
		"""
		Sets the position of the Entity.
		"""
		self.x, self.y = x, y
	
	def get_position_next_to(self):
		"""
		This differs from the Node.js version of the server.
		
		It appears to be a static method -- it doesn't call anything in "this".  It has been changed to be a class method
		of Entity instead.  Additionally, this will return a tuple of values instead of an object position.
		
		This is a "quick and dirty hack" to give mobs a position randomly near another entity.
		"""
		r = randint(0, 3)
		x, y = self.x, self.y
		
		if r == 0:
			y -= 1
		elif r == 1:
			y += 1
		elif r == 2:
			x -= 1
		elif r == 3:
			x += 1
		
		return x, y