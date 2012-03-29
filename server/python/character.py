#!/usr/bin/env python
from entity import Entity
from utils import random_orientation
import message

class Character(Entity):
	def __init__(self, entity_id, entity_type, kind, x, y):
		super(Character, self).__init__(entity_id, entity_type, kind, x, y)
		
		self.orientation = random_orientation()
		self.attackers = {}
		self.target = None
	
	def get_state(self):
		o = super(Character, self).get_state()
		o.append(self.orientation)
		if self.target:
			o.append(self.target)
		
		return o
	
	def reset_hit_points(self, max_hit_points):
		self.hit_points = self.max_hit_points = max_hit_points
	
	def regen_health_by(self, value):
		if self.hit_points < self.max_hit_points:
			self.hit_points += value
			
			if self.hit_points > self.max_hit_points:
				self.hit_points = self.max_hit_points
	
	def has_full_health(self):
		return self.hit_points == self.max_hit_points
		
	def set_target(self, entity):
		self.target = entity.entity_id
	
	def clear_target(self):
		self.target = None
	
	def has_target(self):
		return self.target != None
	
	def attack(self):
		return messages.AttackMessage(self.id, self.target)
	
	def health(self):
		return messages.HealthMessage(self.hit_points, False)
	
	def regen(self):
		return messages.HealthMessage(self.hit_points, True)
		
	def add_attacker(self, entity):
		if entity and not self.attackers.has_key[entity.entity_id]:
			self.attackers[entity.entity_id] = entity
	
	def remove_attacker(self, entity):
		if entity and self.attackers.has_key[entity.entity_id]:
			del self.attackers[entity.entity_id]
