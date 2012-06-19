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
from threading import Thread
from types import ENTITIES
import logging, time
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
		self.ups = 50.
		self.regen_count = self.ups * 2
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
		self.mob_areas = []
		self.chest_areas = []
		self.groups = {}
		
		self.outgoing_queues = {}
		
		self.item_count = self.player_count = 0
		
		self.zone_groups_ready = False
		self.keep_running = True
	
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
	
	def regen_tick(self):
		logger.info('regen_tick called')
		for character in self.characters():
			if not character.has_full_health():
				character.regen_health_by(character.max_hit_points // 25.)
			
			if type(character) == Player:
				self.push_to_player(character, character.regen())
			
	def run(self, map_file_path):
		# this function call is sync in python
		# don't need to wait for callbacks.
		self.map = Map(map_file_path)
		
		# generate_collision_grid called from Map.init_map
		
		self.map.populate_world(self)
		
		# start main loop in another thread
		self.main_loop = Thread(target=self.loop)
		self.main_loop.start()
	
	def loop(self):
		while self.keep_running:
			self.process_groups()
			self.process_queues()
			
			if self.update_count < self.regen_count:
				self.update_count += 1
			else:
				self.regen_tick()
				
				self.update_count = 0
			
			time.sleep(1.0 / self.ups)
		
		
	def characters(self):
		"Returns a list of players and mobs"
		for x in self.players.values():
			yield x
		for x in self.mobs.values():
			yield x
			
	def set_updates_per_seconds(self, ups):
		self.ups = ups
	
	def push_relevant_entity_list_to(self, player):
		entities = []
		
		if player and player.group in self.groups:
			entities = self.groups[player.group].entities.keys()
			if player.entity_id in entities:
				entities.remove(player.entity_id)
			
			# before sending to client, all entities must be an int
			if entities:
				self.push_to_player(player, ListMessage((int(x) for x in entities)))
			
	
	def push_spawns_to_player(self, player, ids):
		"Push entity spawns to the client"
		for eid in ids:
			eid = str(eid)
			if eid in self.entities:
				self.push_to_player(player, SpawnMessage(self.entities[eid]))
	
	def push_to_player(self, player, message):
		if player and player.entity_id in self.outgoing_queues:
			self.outgoing_queues[player.entity_id].append(message)
		else:
			logger.warn('player was undefined')
	
	def push_to_group(self, group, message, ignored_player=None):
		"""
		API change from JS: takes a group as the argument, not a group id
		"""
		#if group_id in self.groups:
		#group = self.groups[group_id]
		for player in group.players:
			if player.entity_id != ignored_player:
				self.push_to_player(player, message)
		#else:
		#	logger.warn('groupid %r is not a valid group' % group_id)
	
	def push_to_adjacent_groups(self, group, message, ignored_player=None):
		"""
		API change from JS: takes a group as the argument, not a group id
		"""
		for g in self.map.get_adjacent_group_positions(group.group_id):
			if g in self.groups:
				self.push_to_group(self.groups[g], message, ignored_player)
	
	def push_to_previous_groups(self, player, message):
		# push this message to all groups which are not going to be updated
		# anymore, as the player left them.
		for g in player.recently_left_groups:
			self.push_to_group(g, message)
		
		player.recently_left_groups = []
	
	def push_broadcast(self, message, ignored_player=None):
		for player_id in self.outgoing_queues:
			if player_id != ignored_player:
				self.outgoing_queues[player_id].append(message)
				
	def process_queues(self):
		for player_id, q in enumerate(self.outgoing_queues):
			player = self.players[player_id]
			for msg in q:
				player.send(q)
			
			q = []

	def add_entity(self, entity):
		self.entities[entity.entity_id] = entity
		self.handle_entity_group_membership(entity)
	
	def remove_entity(self, entity):
		if entity.entity_id in self.entities:
			del self.entities[entity.entity_id]
		
		if entity.entity_id in self.mobs:
			del self.items[entity.entity_id]
			self.clear_mob_aggro_link(entity)
		
		if entity.entity_id in self.items:
			del self.items[entity.entity_id]
		
		entity.destroy()
		self.remove_from_groups(entity)
		
		logger.info('removed entity %r' % entity)
	
	def add_player(self, player):
		self.add_entity(player)
		self.players[player.entity_id] = player
		self.outgoing_queues[player.entity_id] = []
	
	def remove_player(self, player):
		player.broadcast(DespawnMessage(player))
		self.remove_entity(player)
		del self.players[player.entity_id]
		del self.outgoing_queues[player.entity_id]
	
	def add_mob(self, mob):
		self.add_entity(mob)
		self.mobs[mob.entity_id] = mob
	
	def add_npc(self, kind, x, y):
		npc = Npc('8%s%s' % (x, y), kind, x, y)
		self.add_entity(npc)
		self.npcs[npc.entity_id] = npc
		
		return npc
	
	def add_item(self, item):
		self.add_entity(item)
		self.items[item.entity_id] = item
		
		return item
	
	def create_item(self, kind, x, y):
		eid = '9%s' % self.item_count
		self.item_count += 1
		
		if kind == ENTITIES['CHEST']:
			item = Chest(eid, x, y)
		else:
			item = Item(eid, kind, x, y)
		
		return item
	
	def create_chest(self, x, y, items):
		chest = self.create_item(ENTITIES['CHEST'], x, y)
		chest.items = items
		
		return chest
	
	def add_static_item(self, item):
		item.is_static = True
		# TODO: on_respawn handler
		
		self.add_item(item)
	
	def add_item_from_chest(kind, x, y):
		item = self.create_item(kind, x, y)
		item.is_from_chest = True
		
		return self.add_item(item)
	
	def is_valid_position(self, x, y):
		if self.map:
			x, y = int(x), int(y)
			return not (self.map.is_out_of_bounds(x, y) or self.map.is_colliding(x, y))
		
		return False
	
	def process_groups(self):
		if self.zone_groups_ready:
			for gid in self.map.groups():
				group = self.groups[gid]
				
				for entity in group.incoming:
					if type(entity) is Player:
						self.push_to_group(group, SpawnMessage(entity), entity.entity_id)
					else:
						self.push_to_group(group, SpawnMessage(entity))
				
				group.incoming = []
	
	def try_adding_mob_to_chest_area(self, mob):
		for area in self.chest_areas:
			if area.contains(mob):
				area.add_to_area(mob)

	def add_to_group(self, entity, group):
		new_groups = []
		
		for group_id in self.map.get_adjacent_group_positions(group.group_id):
			# FIXME: memory leak?
			if group_id not in self.groups:
				logger.warn('Invalid group id referenced by add_to_group: %r', group_id)
				continue
				
			self.groups[group_id].entities[entity.entity_id] = entity;
			new_groups.append(group_id)
		
		entity.group = group.group_id
		
		return new_groups
	
	def remove_from_groups(self, entity):
		old_groups = []
		
		if entity.group:
			group = self.groups[entity.group]
			
			if entity in group.players:
				group.players.remove(entity)
			
			for group_id in self.map.get_adjacent_group_positions(group.group_id):
				if group_id in self.groups and entity.entity_id in self.groups[group_id].entities:
					del self.groups[group_id].entities[entity.entity_id]
					old_groups.append(group_id)
			
			entity.group = None
		
		return old_groups
	
	def handle_entity_group_membership(self, entity):
		has_changed_groups = False
		
		if entity:
			group_id = self.map.get_group_id_from_position(entity.x, entity.y)
			group = self.groups[group_id]
			
			if not entity.group or (entity.group != group):
				has_changed_groups = True
				
				self.add_as_incoming_to_group(entity, group)
				old_groups = set(self.remove_from_groups(entity))
				new_groups = set(self.add_to_group(entity, group))
				
				if old_groups:
					old_groups -= new_groups
					entity.recently_left_groups = old_groups
					
					logger.info('group diff: %r', entity.recently_left_groups)
					
		return has_changed_groups
	
	def add_as_incoming_to_group(self, entity, group):
		"""
		Registers an entity as incoming into several groups, meaning that it
		just entered them.  All players inside these groups will recieve a
		Spawn message when World.process_groups() is called.
		"""
		
		is_chest = type(entity) is Chest
		is_item = type(entity) is Item
		is_dropped_item = is_item and not (entity.is_static or entity.is_from_chest)
		
		for group_id in self.map.get_adjacent_group_positions(group.group_id):
			if group_id in self.groups:
				group = self.groups[group_id]
				
				if entity in group.entities and (not is_item or is_chest or (is_item and not is_dropped_item)):
					group.incoming.append(entity)
			else:
				logger.warn('Invalid group id referenced by add_as_incoming_to_group: %r', group_id)
	
	def push_relevant_entities(self, player):
		# TODO: stub
		pass
		