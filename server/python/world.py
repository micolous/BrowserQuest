#!/usr/bin/env python
from character import Character
from player import Player
from mob import Mob
from message import *
from map import Map
from math import floor
from npc import Npc
from chest import Chest
from item import Item
import logging
logger = logging.getLogger(__name__)

class World(object):
	"""
	Defines a shard of the world.
	
	This is equivalent to js/worldserver.js:World
	"""
	def __init__(self, world_id, max_players, server):
		self.world_id = world_id
		self.max_players = max_players
		self.server = server
		
		# updates per second.
		self.ups = 50
		self.regenCount = self.ups * 2
		self.update_count = 0
		
		self.map = None
		
		self.entities = {}
		self.players = {}
		self.mobs = {}
		self.attackers = {}
		self.items = {}
		self.equipping = {}
		self.hurt = {}
		self.npcs = {}
		self.mob_areas = {}
		self.chest_areas = {}
		self.groups = {}
		
		self.outgoing_queues = {}
		
		self.item_count = self.player_count = 0
		
		self.zone_groups_ready = False
	
	def on_player_connect(self, player):
		def on_request_position():
			if player.last_checkpoint:
				return player.last_checkpoint.get_random_position()
			else:
				return self.map.get_random_starting_position()
				
		player.on_request_position = on_request_position
	
	def on_player_enter(self, player):
		logger.info("%s has joined world %d", player.name, self.world_id)
		player.world = self
		
		if not player.has_entered_game:
			self.player_count += 1
		
		# send the population and relevant entities in this world
		player.send(PopulationMessage(self.player_count))
		self.push_relevant_entities(player)
		
		if self.added_callback:
			self.added_callback()
	
	def on_entity_attack(self, attacker):
		"Called when an entity is attacked by another entity."
		target = self.get_entity_by_id(attacker.target)
		
		if target and type(attacker) is Mob:
			pos = self.find_position_next_to(attacker, target)
			self.move_entity(attacker, *pos)
	
	def on_regen_tick(self):
		for character in self.characters():
			if not character.has_full_health():
				character.regen_health_by(floor(character.max_hit_points / 25.))
			
			if type(character) == Player:
				self.push_to_player(character, character.regen())
			
	def run(self, map_file_path):
		# this function call is sync in python
		# don't need to wait for callbacks.
		self.map = Map(map_file_path)
		
		# generate_collision_grid called from Map.init_map
		
		# populate mob roaming areas
		
		
	def characters(self):
		"Returns a list of players and characters"
		for x in self.characters.values():
			yield x
		for x in self.mobs.values():
			yield x
			
	def set_updates_per_seconds(self, ups):
		self.ups = ups
	
	def push_relevant_entity_list_to(self, player):
		entities = []
		
		# TODO: implement
	
	def push_spawns_to_player(self, player, ids):
		"Push entity spawns to the client"
		# TODO: implement
	
	def add_player(self, player):
		self.add_entity(player)
		self.players[player.entity_id] = player
		
	def add_entity(self, entity):
		self.entities[entity.entity_id] = entity
	
	def add_mob(self, mob):
		self.add_entity(mob)
		self.mobs[mob.entity_id] = mob
	
	def add_npc(self, kind, x, y):
		npc = Npc('8-%s-%s-%s' % (kind, x, y), kind, x, y)
		self.add_entity(npc)
		self.npcs[npc.entity_id] = npc
		
		return npc
	
	def add_item(self, item):
		self.add_entity(item)
		self.items[item.entity_id] = item
		
		return item
	
	def create_item(self, kind, x, y):
		eid = '9-%s' % self.item_count
		self.item_count += 1
		
		if kind == ENTITIES['CHEST']:
			item = Chest(eid, x, y)
		else:
			item = Item(eid, kind, x, y)
		
		return item
	
	def create_chest(self, x, y, items):
		chest = self.create_item(ENTITIES['CHEST'], x, y)
		chest.set_items(items)
		
		return chest
	
	def add_static_item(self, item):
		item.is_static = True
		# TODO: on_respawn handler
		
		self.add_item(item)
	
	def add_item_from_chest(kind, x, y):
		item = self.create_item(kind, x, y)
		item.is_from_chest = True
		
		return self.add_item(item)
	