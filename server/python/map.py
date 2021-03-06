#!/usr/bin/env python
from math import floor
from random import choice
from checkpoint import Checkpoint
from mobarea import MobArea
from chestarea import ChestArea
from mob import Mob
from types import *
from group import Group, ZONE_WIDTH, ZONE_HEIGHT
import logging, json
logger = logging.getLogger(__name__)

class Map(object):
	def __init__(self, map_file):
		"Loads up the map.  Unlike the JS version, this is not async."
		self.is_loaded = False
		
		try:
			data = json.load(open(map_file, 'rb'))
		except IOError:
			logger.error('Failure loading map %s', map_file)
		else:
			self.init_map(data)
	
	def init_map(self, map):
		self.width, self.height = map['width'], map['height']
		self.collisions = map['collisions']
		self.mob_areas = map['roamingAreas']
		self.chest_areas = map['chestAreas']
		self.static_chests = map['staticChests']
		self.static_entities = map['staticEntities']
		self.is_loaded = True
		
		# this is static information, doesn't need to be in a class.
		#self.zone_width, self.zone_height = 28, 12
		self.group_width = self.width // ZONE_WIDTH
		self.group_height = self.height // ZONE_HEIGHT
		self.init_connected_groups(map['doors'])
		self.init_checkpoints(map['checkpoints'])
		self.generate_collision_grid()
	
	def tile_index_to_grid_position(self, tile_number):
		if tile_number == 0:
			x = 0
		else:
			if (tile_number % self.width) == 0:
				x = self.width - 1
			else:
				x = (tile_number % self.width) - 1
		
		tile_number -= 1
		y = int(floor(tile_number / float(self.width)))
		
		return x, y
	
	def grid_position_to_tile_index(self, x, y):
		return (y * self.width) + x + 1
	
	def generate_collision_grid(self):
		self.grid = {}
		
		if self.is_loaded:
			tile_index = 0
			for i in range(self.height):
				self.grid[i] = {}
				for j in range(self.width):
					self.grid[i][j] = tile_index in self.collisions
					tile_index += 1
	
	def is_out_of_bounds(self, x, y):
		return x <= 0 or x >= self.width or y <= 0 or y >= self.height
	
	def is_colliding(self, x, y):
		if self.is_out_of_bounds(x, y):
			return False
			
		return self.grid[y][x]
	
	def group_id_to_group_position(self, group_id):
		return [int(x) for x in group_id.split('-', 2)]
	
	def get_group_id_from_position(self, x, y):
		return '%d-%d' % (
			(x - 1) // ZONE_WIDTH,
			(y - 1) // ZONE_HEIGHT
		)
	
	def groups(self):
		for x in range(self.group_width):
			for y in range(self.group_height):
				yield '%d-%d' % (x, y)
	
	def get_adjacent_group_positions(self, group_id):
		pos = self.group_id_to_group_position(group_id)
		groups = set()
		
		# surrounding groups
		for x in range(3):
			for y in range(3):
				groups.add(self.get_group_id_from_position(pos[0] + (x - 1), pos[1] + (y - 1)))
		
		# groups connected via doors
		if group_id in self.connected_groups:
			for pos in self.connected_groups[group_id]:
				# sets automatically discard duplicates
				[groups.add(p) for p in pos]
			
		# remove groups that are outside of the range, and generate a new list.
		for group in groups:
			if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.group_width and pos[1] < self.group_height:
				yield group
	
	def init_connected_groups(self, doors):
		self.connected_groups = {}
		
		for door in doors:
			group_id = self.get_group_id_from_position(door['x'], door['y'])
			connected_group_id = self.get_group_id_from_position(door['tx'], door['ty'])
			connected_position = self.group_id_to_group_position(connected_group_id)
			
			if group_id not in self.connected_groups:
				self.connected_groups[group_id] = []
				
			self.connected_groups[group_id].append(connected_position)
				
	def init_checkpoints(self, cp_list):
		self.checkpoints = {}
		self.starting_areas = []
		
		for cp in cp_list:
			checkpoint = Checkpoint(cp['id'], cp['x'], cp['y'], cp['w'], cp['h'])
			
			self.checkpoints[checkpoint.checkpoint_id] = checkpoint
			if cp['s']:
				self.starting_areas.append(checkpoint)
	
	def get_random_starting_position(self):
		area = choice(self.starting_areas)
		
		return area.get_random_position()
	
	def init_zone_groups(self, world):
		# from Server.initZoneGroups
		for group_id in self.groups():
			world.groups[group_id] = Group(group_id, world)
	
	def populate_world(self, world):
		self.init_zone_groups(world)
	
		# from worldserver.js:World.run.map.ready
		# populate all mob "roaming" areas
		for a in self.mob_areas:
			area = MobArea(a['id'], a['nb'], a['type'], a['x'], a['y'], a['width'], a['height'], world)
			world.mob_areas.append(area)
			area.spawn_mobs()
			
			# TODO: empty handler
		
		# create all chest areas
		for i, a in enumerate(self.chest_areas):
			# BUG: map contains no thing called "id".  possibly undefined
			area = ChestArea(i, a['x'], a['y'], a['w'], a['h'], a['tx'], a['ty'], a['i'], world)
			world.chest_areas.append(area)
			
			# TODO: empty handler
		
		# spawn static chests
		for chest in self.static_chests:
			c = world.create_chest(chest['x'], chest['y'], chest['i'])
			world.add_static_item(c)
		
		# spawn static entities
		self.spawn_static_entities(world)
		
		# set max number of entities contained in each chest area
		for area in world.chest_areas:
			area.set_number_of_entities(len(area.entities))
	
	def spawn_static_entities(self, world):
		# from worldserver.js:World.spawnStaticEntities
		count = 0
		for tid, k in self.static_entities.iteritems():
			kind = ENTITIES[k.upper()]
			x, y = self.tile_index_to_grid_position(int(tid))
			
			if is_npc(kind):
				world.add_npc(kind, x + 1, y)
			elif is_mob(kind):
				mob = Mob('7%s%s' % (kind, count), kind, x + 1, y)
				count += 1
				
				# TODO: respawn code
				
				world.add_mob(mob)
				world.try_adding_mob_to_chest_area(mob)
			elif is_item(kind):
				world.add_static_item(world.create_item(kind, x + 1, y))
				

