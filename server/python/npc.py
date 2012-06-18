#!/usr/bin/env python
from entity import Entity


class Npc(Entity):
	def __init__(self, entity_id, kind, x, y):
		super(Npc, self).__init__(entity_id, 'npc', kind, x, y)
