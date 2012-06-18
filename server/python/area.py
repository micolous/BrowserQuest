#!/usr/bin/env python
from random import randint
from mob import Mob

class Area(object):
	def __init__(self, area_id, x, y, width, height, world):
		self.area_id = area_id
		self.x, self.y = x, y
		self.width, self.height = width, height
		self.world = world
		
		self.entities = {}
		self.has_completely_respawned = True
		self.empty_callback = None
	
	def get_random_position_inside_area(self):
		x, y = self.x, self.y
		valid = False
		
		while not valid:
			x = self.x + randint(0, self.width + 1)
			y = self.y + randint(0, self.height + 1)
			valid = self.world.is_valid_position(x, y)
		
		return x, y
	
	def remove_from_area(self, entity):
		if self.entities.has_key(entity.entity_id):
			del self.entities[entity.entity_id]
		
		if self.entities and self.has_completely_respawned and self.empty_callback:
			self.has_completely_respawned = False
			self.empty_callback()
		
	def add_to_area(self, entity):
		self.entities[entity.entity_id] = entity
		entity.area = self
		
		if type(entity) is Mob:
			self.world.add_mob(entity)
		
		if self.is_full():
			self.has_completely_respawned = True
		
	def set_number_of_entities(self, num):
		self.number_of_entities = num
	
	def is_empty(self):
		for ent in self.entities.itervalues():
			if ent.is_dead:
				return False
		
		return True
	
	def is_full(self):
		return not self.is_empty() and self.number_of_entities >= len(self.entities)
	
	def on_empty(self, callback):
		self.empty_callback = callback
