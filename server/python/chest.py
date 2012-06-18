#!/usr/bin/env python
from item import Item
from types import ENTITIES
from random import choice

class Chest(Item):
	def __init__(self, entity_id, x, y):
		super(Chest, self).__init__(entity_id, ENTITIES['CHEST'], x, y)
		self.items = []
	
	def get_random_item(self):
		if self.items:
			return choice(self.items)
