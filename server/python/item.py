#!/usr/bin/env python

class Item(object):
	def __init__(self, entity_id, kind, x, y):
		super(Item, self).__init__(entity_id, 'item', kind, x, y)
		self.is_static = False
		self.is_from_chest = False
		self.on_respawn = None
	
	def handle_despawn(self, params):
		# this appears in the node.js version to implement some sort of blink
		# out, server side... wtf?
		
		pass
	
	def destroy(self):
		if self.is_static:
			self.schedule_respawn(30)
		
	def schedule_respawn(self, delay)
		# TODO: schedule this for the future, rather than processing
		# immediately.
		if callable(self.on_respawn):
			self.on_respawn(self)
