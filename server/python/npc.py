#!/usr/bin/env python
from entity import Entity


class Npc(object):
	def __init__(self, entity_id, kind, x, y):
		super(Npc, self).__init__(self, entity_id, 'npc', kind, x, y)
