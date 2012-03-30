#!/usr/bin/env python
import logging, json
logger = logging.getLogger(__name__)


class Map(object):
	def __init__(self, map_file):
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
		#self.