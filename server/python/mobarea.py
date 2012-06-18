#!/usr/bin/env python
from area import Area
from mob import Mob
from types import ENTITIES

class MobArea(Area):
	def __init__(self, area_id, nb, kind, x, y, width, height, world):
		super(MobArea, self).__init__(area_id, x, y, width, height, world)
		
		self.nb = nb
		self.kind = kind
		assert kind.upper() in ENTITIES, 'Unknown entity type %r' % kind
		
		self.respawns = []
		self.set_number_of_entities(nb)
		
	def spawn_mobs(self):
		for x in range(self.nb):
			self.add_to_area(self.create_mob_inside_area())
	
	def create_mob_inside_area(self):
		x, y = self.get_random_position_inside_area()
		k = ENTITIES[self.kind.upper()]
		mob = Mob('1%s%s%s' % (self.area_id, k, len(self.entities)), k, x, y)
		
		#mob.on_move = self.world.on_mob_move_callbacks.append(mob)
		return mob