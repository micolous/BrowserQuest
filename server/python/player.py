#!/usr/bin/env python
from message import MESSAGES, WelcomeMessage
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
		
		# TODO: fix this to use proper ID assignment.
		connection_id = randint(0, 65535)
		super(Player, self).__init__(connection_id, "player", ENTITIES['WARRIOR'], 0, 0)
		
		self.is_dead = False
		self.has_entered_game = False
		
		
	def handle_message(self, message):
		logger.info('Recieved: %r', message)
		
		action = int(message[0])
		
		if action == MESSAGES['HELLO']:
			if self.has_entered_game and not self.is_dead:
				self.connection.close('Cannot initiate handshake twice!')
			else:
				# we can accept this hello.
				
				# TODO: implement sanitiser.
				if message[1] == '':
					self.name = 'Leeroy Jenkins'
				else:
					self.name = message[1][:16]
				
				self.kind = ENTITIES['WARRIOR']
				self.equip_armor(message[2])
				self.equip_weapon(message[3])
				self.orientation = random_orientation()
				self.update_hit_points()
				self.update_position()
				
				self.server.add_player(self)
				#self.server.
				
				# send welcome message
				self.send(WelcomeMessage(self).serialise())
				self.has_entered_game = True
				self.is_dead = False
			
		elif self.has_entered_game:
		
			logger.warn('Ignoring unknown message type %d during has_entered_game', action)
		else:
			logger.warn('Ignoring message type %d during !has_entered_game', action)
		
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
		
		s = json.dumps(message)
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
		# TODO: implement requestpos_callback
		pass
	
		
		