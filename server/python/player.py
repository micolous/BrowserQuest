#!/usr/bin/env python
from message import *
from character import Character
from utils import random_orientation
from properties import get_armor_level, get_weapon_level
from types import ENTITIES
from random import randint
import formulae

import logging, json
logger = logging.getLogger(__name__)

class Player(Character):
	"""
	Represents a player and their connection to the server.
	
	Responsible for parsing new messages from the client and handling connectivity.
	
	"""
	def __init__(self, connection, server):
		self.connection = connection
		self.server = server
		self.world = None
		
		# TODO: fix this to use proper ID assignment.
		connection_id = randint(0, 65535)
		super(Player, self).__init__(connection_id, "player", ENTITIES['WARRIOR'], 0, 0)
		
		self.is_dead = False
		self.has_entered_game = False
		self.haters = {}
		self.last_checkpoint = None
		self.on_request_position = None
		
		
	def handle_message(self, message_data):
		logger.info('Recieved: %r', message_data)
		msg = deserialise_message(message_data)
		
		if type(msg) is HelloMessage:
			if self.has_entered_game and not self.is_dead:
				self.connection.close('Cannot handshake twice!')
			else:
				# we can accept this hello.
				
				# TODO: implement sanitiser.
				if msg.player_name == '':
					self.name = 'Leeroy Jenkins'
				else:
					self.name = msg.player_name[:16]
				
				self.kind = ENTITIES['WARRIOR']
				self.equip_armor(msg.armor_kind)
				self.equip_weapon(msg.weapon_kind)
				self.orientation = random_orientation()
				self.update_hit_points()
				self.update_position()
				
				self.server.add_player(self)
				#self.server.
				
				# send welcome message
				self.send(WelcomeMessage(self))
				self.has_entered_game = True
				self.is_dead = False
		elif self.has_entered_game:
			if type(msg) is ChatMessage:
				# ignore the player_id sent by the client
				
				# TODO: broadcast this to nearby clients.
				logger.info('<%s> %s', self.name, msg.message)
			elif type(msg) is MoveMessage:
				# TODO: broadcast this.
				logger.info('%s moved to %r, %r', self.name, msg.x, msg.y)
			elif type(msg) is CheckMessage:
				# TODO: handle this properly
				logger.info('%s checkpoint is %r', self.name, msg.checkpoint_id)
			else:
				logger.warn('Ignoring unknown message type %d (%s) during has_entered_game', msg.message_type, msg.message_type_label())
		else:
			logger.warn('Ignoring message type %d (%s) during !has_entered_game', msg.message_type, msg.message_type_label())
		
	def destroy(self):
		for mob in self.attackers.values():
			mob.clear_target()
		
		self.attackers = []
		
		# TODO: haters aren't implemented yet.
	
	def get_state(self):
		o = super(Player, self).get_state() + [
			self.name,
			self.orientation,
			self.armor,
			self.weapon
		]
		
		if self.target:
			o.append(this.target)
		
		return o
		
	def send(self, message):
		s = json.dumps(message.serialise())
		self.connection.send_message(s, binary=False)
	
	def equip_armor(self, kind):
		self.armor = kind
		self.armor_level = get_armor_level(kind)
	
	def equip_weapon(self, kind):
		self.weapon = kind
		self.weapon_level = get_weapon_level(kind)
	
	def update_hit_points(self):
		self.reset_hit_points(formulae.hp(self.armor_level))
	
	def update_position(self):
		# the World registers a callback to set the starting position of the player.
		logger.info('Player.update_position called, on_request_position = %s', self.on_request_position)
		if callable(self.on_request_position):
			pos = self.on_request_position()
			self.set_position(*pos)
	
	def on_move(self, x, y):
		# moved from worldserver.js
		logger.debug('%s is moving to (%d, %d)', self.name, x, y)
		
		for attacker in self.attackers.values():
			target = self.world.get_entity_by_id(attacker.target)
			
			if target:
				pos = self.world.find_position_next_to(attacker, target)
				
				if attacker.distance_to_spawning_point(*pos) > 50:
					attacker.clear_target()
					attacker.forget_everyone()
					self.remove_attacker(attacker)
				else:
					self.world.move_entity(attacker, *pos)
					
	on_loot_move = on_move
	
	def on_zone(self):
		has_changed_group = self.world.handle_entity_group_membership(self)
		
		if has_changed_group:
			self.world.push_to_previous_groups(self, DestroyMessage(self))
			self.world.push_relevant_entities(self)
			
	def on_broadcast(self, message, ignore_self):
		if ignore_self:
			entity_id = None
		else:
			entity_id = self.entity_id
		
		self.world.push_to_adjacent_groups(self.group, message, entity_id)
	
	def on_broadcast_to_zone(self, message, ignore_self):
		if ignore_self:
			entity_id = None
		else:
			entity_id = self.entity_id
		
		self.world.push_to_group(self.group, message, entity_id)
	
	def on_exit(self):
		logger.info('%s has left the game.', self.name)
		
		self.world.remove_player(player)
		self.world.player_count -= 1
		
		if self.world.removed_callback:
			self.world.removed_callback()
		
		
	