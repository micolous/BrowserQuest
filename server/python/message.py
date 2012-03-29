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

class AttackMessage(Message):
	message_type = MESSAGES['ATTACK']
	
	def __init__(self, attacker_id, target_id):
		self.attacker_id = attacker_id
		self.target_id = target_id
	
	def serialise(self):
		return super(AttackMessage, self).serialise() + [
			self.attacker_id,
			self.target_id
		]

class HealthMessage(Message):
	message_type = MESSAGES['HEALTH']
	
	def __init__(self, points, is_regen):
		self.points = points
		self.is_regen = is_regen
	
	def serialise(self):
		o = super(AttackMessage, self).serialise() + [self.points]
		if self.is_regen:
			o.append(1)
		
		return o

class WelcomeMessage(Message):
	"node.js version implements this in player.js:Player.connection.listen.  Implemented here for consistancy."
	message_type = MESSAGES['WELCOME']
	
	def __init__(self, player):
		self.player = player
	
	def serialise(self):
		return super(WelcomeMessage, self).serialise() + [
			self.player.entity_id,
			self.player.name,
			self.player.x,
			self.player.y,
			self.player.hit_points
		]
	