#!/usr/bin/env python
from player import Player
from world import World
import json
import logging
logger = logging.getLogger(__name__)

class Server(object):
	def __init__(self):
		"""
		This is called when mod_pywebsockets imports the _wsh handler.
		
		This is somewhat equivalent to some of the stuff in /server/js/main.js.
		"""
		# TODO: implement configuration.
		# We implement an unsharded world.
		self.world = World(1, 64, self)
		
		
		self.world.run("./server/maps/world_server.json")
		
		
		
		self.clients = []
	
	def add_player(self, player):
		self.clients.append(player)
	
	
	def do_extra_handshake(self, request):
		"""
		TODO: Implement checks on request origins.
		"""
		
		pass
	
	def transfer_data(self, request):
		"""
		This is called when a WebSockets connection is created on the server.
		"""
		#logger.info('running inside of server %s', self)
		player = Player(request.ws_stream, self)
		self.world.on_player_connect(player)
		
		# tell the client it's okay to start sending us stuff
		request.ws_stream.send_message('go')
		
		while True:
			
			data = request.ws_stream.receive_message()
			logger.info('got client message: %r', data)
			if data is None:
				# disconnect
				return
			
			# we don't implement BiSON
			msg = json.loads(data)
			player.handle_message(msg)
			