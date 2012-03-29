#!/usr/bin/env python
from player import Player
import json
import logging
logger = logging.getLogger(__name__)

class Server(object):
	def __init__(self):
		self.clients = []
		pass
	
	def add_player(self, player):
		self.clients.append(player)
	
	
	def do_extra_handshake(self, request):
		# do nothing, accept everything for now.
		pass
	
	def transfer_data(self, request):
		# this is our main event loop
		logger.info('running inside of server %s', self)
		player = Player(request.ws_stream, self)
		
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
			