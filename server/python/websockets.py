#!/usr/bin/env python
import logging
logger = logging.getLogger(__name__)

class Server(object):
	def __init__(self):
		self.clients = []
		pass
		
	def do_extra_handshake(self, request):
		# do nothing, accept everything for now.
		pass
	
	def transfer_data(self, request):
		# this is our main event loop
		logger.info('running inside of server %s', self)
		while True:
			line = request.ws_stream.receive_message()
			if line is None:
				# disconnect
				return
			
			logger.info('client got data: %r', line)
			