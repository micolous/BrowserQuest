#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)

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

MESSAGE_HANDLERS = {}

def message_handler(cls):
	"Decorator to register various message handling functionality."
	assert hasattr(cls, 'deserialise'), "%r does not implement required deserialise method" % cls
	assert hasattr(cls, 'message_type'), "%r does not implement required message_type attribute" % cls
	
	MESSAGE_HANDLERS[cls.message_type] = cls
	return cls
	
def deserialise_message(msg):
	msg[0] = int(msg[0])
	if MESSAGE_HANDLERS.has_key(msg[0]):
		return MESSAGE_HANDLERS[msg[0]].deserialise(msg)
	else:
		logging.warn("Undecodable message type %r recieved.", msg[0])
		m = Message()
		m.message_type = msg[0]
		return m

class Message(object):
	message_type = None
	def serialise(self):
		return [self.message_type]
	
	def message_type_label(self):
		"Used for debugging server implementation by printing the event packet by name."
		try:
			return [k for k, v in MESSAGES.iteritems() if v == self.message_type][0]
		except:
			return None

@message_handler
class HelloMessage(Message):
	message_type = MESSAGES['HELLO']
	
	def __init__(self, player_name, armor_kind, weapon_kind):
		self.player_name = player_name
		self.armor_kind = armor_kind
		self.weapon_kind = weapon_kind
	
	def serialise(self):
		"Not used by the server, but implemented anyway for testing."
		return super(HelloMessage, self).serialise() + [
			self.player_name,
			self.armor_kind,
			self.weapon_kind
		]

	@classmethod
	def deserialise(cls, msg):
		return cls(msg[1], msg[2], msg[3])


class SpawnMessage(Message):
	message_type = MESSAGES['SPAWN']
	
	def __init__(self, entity):
		self.entity = entity
	
	def serialise(self):
		return super(SpawnMessage, self).serialise() + self.entity.get_state()
	
	
class DespawnMessage(Message):
	message_type = MESSAGES['DESPAWN']
	
	def __init__(self, entity):
		self.entity_id = entity.entity_id
	
	def serialise(self):
		return super(DespawnMessage, self).serialise() + [self.entity_id]

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

@message_handler
class ChatMessage(Message):
	message_type = MESSAGES['CHAT']
	
	def __init__(self, player=None, message="", entity_id=0):
		if player:
			self.entity_id = player.entity_id
		else:
			self.entity_id = entity_id
		self.message = message
	
	def serialise(self):
		return super(ChatMessage, self).serialise() + [
			self.entity_id,
			self.message
		]

	@classmethod
	def deserialise(cls, msg):
		"For client->server messages, the entity_id sent should be ignored!"
		return cls(entity_id=msg[1], message=msg[2])

class DestroyMessage(DespawnMessage):
	message_type = MESSAGES['DESTROY']

@message_handler
class MoveMessage(Message):
	"""
	Represents an entity's movement in the world.
	
	This has been modified from the original protocol.
	
	Client->Server message is now the same as the Server->Client message.
	"""
	message_type = MESSAGES['MOVE']
	
	def __init__(self, entity=None, x=0, y=0, entity_id=0):
		if entity:
			self.entity_id = entity.entity_id
		else:
			self.entity_id = entity_id
		
		self.x, self.y = x, y

	def serialise(self):
		return super(ChatMessage, self).serialise() + [
			self.entity_id,
			self.x, 
			self.y
		]
	
	@classmethod
	def deserialise(cls, msg):
		return cls(entity_id=msg[1], x=msg[2], y=msg[3])

@message_handler
class CheckMessage(Message):
	"""
	Notifies the server of the client's current checkpoint.
	
	"""
	message_type = MESSAGES['CHECK']
	
	def __init__(self, checkpoint_id=0):
		self.checkpoint_id = checkpoint_id
	
	def serialise(self):
		return super(CheckMessage, self).serialise() + [
			self.checkpoint_id
		]
	
	@classmethod
	def deserialise(cls, msg):
		return cls(checkpoint_id=msg[1])

