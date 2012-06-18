#!/usr/bin/env python
from area import Area


class ChestArea(Area):
	def __init__(self, entity_id, x, y, width, height, cx, cy, items, world):
		super(ChestArea, self).__init__(entity_id, x, y, width, height, world)
		self.items = items
		self.chest_x = cx
		self.chest_y = cy
	
	def contains(self, entity):
		if entity:
			return (
				entity.x >= self.x and
				entity.y >= self.y and
				entity.x < (this.x + this.width) and
				entity.y < (this.y + this.height)
			)
		return False
	