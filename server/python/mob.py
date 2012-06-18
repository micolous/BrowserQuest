#!/usr/bin/env python
from character import Character
from properties import *
from message import *
import utils 

class Mob(Character):
	def __init__(self, entity_id, kind, x, y):
		super(Mob, self).__init__(entity_id, "mob", kind, x, y)
		
		self.update_hit_points()
		
		self.spawn_x, self.spawn_y = x, y
		self.armor_level = get_armor_level(this.kind)
		self.weapon_level = get_weapon_level(this.kind)
		
		self.hate_list = {}
		self.respawn_timeout = None
		self.return_timeout = None
		self.is_dead = False
		self.area = None
		self.on_move = None
		
	def destroy(self):
		self.is_dead = True
		self.hate_list = []
		self.clear_target()
		self.update_hit_points()
		self.reset_position()
		self.handle_respawn()
		
	def recieve_damage(self, points, player):
		self.hit_points -= points
	
	def hates(self, player):
		for p in self.hate_list.iterkeys():
			if p == self.player.entity_id:
				return True
		return False
		
	def increase_hate_for(self, player, points):
		if self.hate_list.has_key(player.entity_id):
			# player exists in hate list.
			self.hate_list[player.entity_id] += points
		else:
			# player doesn't exist in hate list
			self.hate_list[player.entity_id] = points
	
		if self.return_timeout:
			# prevent mob from returning to the spawn because
			# a player has aggroed it
			
			# TODO: implement this.
			pass
	
	def get_hated_player_id(self, hate_rank):
		# TODO: implement this.
		pass
		
	def forget_player(self, player, duration):
		if self.hate_list.has_key(player.entity_id):
			del self.hate_list[player.entity_id]
		
		if not self.hate_list:
			self.return_to_spawning_position(duration)
	
	def forget_everyone(self):
		self.hate_list = {}
		self.return_to_spawning_position(1)
	
	def drop(self, item):
		return DropMessage(self, item)
	
	def handle_respawn(self):
		delay = 30000
		
		if self.area and type(self.area) == MobArea:
			self.area.respawn_mob(self, delay)
		else:
			if self.area and type(self.area) == ChestArea:
				self.area.remove_from_area(self)
			
			# TODO: set respawn timer.
	
	def reset_position():
		self.set_position(self.spawn_x, self.spawn_y)
	
	def return_to_spawning_position(self, duration=4000):
		self.clear_target()
		
		# TODO: implement return timeout
	
	def move(self, x, y):
		self.set_position(x, y)
		
		# TODO: implement move callback
		if callable(self.on_move):
			self.on_move(self)
	
	def update_hit_points(self):
		self.reset_hit_points(get_hit_points(self.kind))
	
	def distance_to_spawning_point(self, x, y):
		return utils.distance_to(x, y, self.spawn_x, self.spawn_y)
	