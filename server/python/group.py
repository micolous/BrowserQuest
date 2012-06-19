#!/usr/bin/env python

# from map.js:Map.initMap
ZONE_WIDTH, ZONE_HEIGHT = 28, 12


class Group(object):
	"""
	Defines a zone (group) of the map.
	
	"""
	entities = {}
	players = []
	incoming = []
	
	def __init__(self, group_id, world):
		self.group_id = group_id
		self.world = world
