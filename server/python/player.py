#!/usr/bin/env python
import message

class Player(object):
	"""
	Represents a player and their connection to the server.
	
	Responsible for parsing new messages from the client and handling connectivity.
	
	"""
	def __init__(self, connection, server):
		self.connection = connection
		self.server = server
		
		self.is_dead = False
		self.has_entered_game = False
		
		
	def handle_message(self, message):
		pass