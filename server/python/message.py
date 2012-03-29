#!/usr/bin/env python

MESSAGES = dict(
	HELLO = 0,
	WELCOME = 1,
	SPAWN = 2,
	DESPAWN = 3,
	MOVE = 4,
	LOOTMOVE = 5,
	AGGRO = 6,
	ATTACK = 7,
	HIT = 8,
	HURT = 9,
	HEALTH = 10,
	CHAT = 11,
	LOOT = 12,
	EQUIP = 13,
	DROP = 14,
	TELEPORT = 15,
	DAMAGE = 16,
	POPULATION = 17,
	KILL = 18,
	LIST = 19,
	WHO = 20,
	ZONE = 21,
	DESTROY = 22,
	HP = 23,
	BLINK = 24,
	OPEN = 25,
	CHECK = 26
)

class Message(object):
	def serialise(self):
		return [self.message_type]

class SpawnMessage(Message):
	message_type = MESSAGES['SPAWN']
	
	def __init__(self, entity):
		self.entity = entity
	
	def serialise(self):
		return super(SpawnMessage, self).serialise() + self.entity.get_state()
	
class DespawnMessage(Message):
	message_type = MESSAGES['DESPAWN']
	
	def __init__(self, entity_id):
		self.entity_id = entity_id
	
	def serialise(self):
		return super(DespawnMessage, self).serialise() + [self.entity_id]

class MoveMessage(Message):
	message_type = MESSAGES['MOVE']
	def __init__(self, entity):
		self.entity = entity
	
	def serialise(self):
		return super(MoveMessage, self).serialise() + [
			self.entity.id,
			self.entity.x,
			self.entity.y
		]

class PopulationMessage(Message):
	message_type = MESSAGES['POPULATION']
	
	def __init__(self, world, total):
		self.world = world
		self.total = total
	
	def serialise(self):
		return super(PopulationMessage, self).serialise() + [
			self.world,
			self.total
		]
