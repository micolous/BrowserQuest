#!/usr/bin/env python
from math import floor
from random import choice
from checkpoint import Checkpoint
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
		
		self.zone_width, self.zone_height = 28, 12
		self.init_connected_groups(map['doors'])
		self.init_checkpoints(map['checkpoints'])
	
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
				for k in range(self.width):
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
			floor((x - 1) / floor(self.zone_width)),
			floor((y - 1) / floor(self.zone_width))
		)
	
	def get_adjacent_group_positions(self, group_id):
		pos = self.group_id_to_group_position(group_id)
		groups = set()
		
		# surrounding groups
		for x in range(3):
			for y in range(3):
				groups.add([pos[0] + (x - 1), pos[1] + (y - 1)])
		
		# groups connected via doors
		for pos in self.connected_groups[group_id]:
			# sets automatically discard duplicates
			groups.add(pos)
			
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
