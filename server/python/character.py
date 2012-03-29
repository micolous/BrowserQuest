#!/usr/bin/env python
from entity import Entity
from utils import random_orientation

class Character(Entity):
	def __init__(self, entity_id, entity_type, kind, x, y):
		super(Character, self).__init__(entity_id, entity_type, kind, x, y)
		
		self.orientation = random_orientation()
		self.attackers = []
		self.target = None
	