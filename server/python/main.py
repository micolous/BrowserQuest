#!/usr/bin/env python
#from worldserver import WorldServer
#from websockets import WebSocketGameConnection, GameServer
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import logging

# TODO: implement configurable logging system
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')	
logger = logging.getLogger(__name__)

def main(config):
	logger.info("Starting the game server...")

	#server = GameServer()
	def request_handler(environ, start_response):
		path = environ['PATH_INFO']
		logger.info("Got request for %r", path)
		
		if path == '/':
			homepage = """
				<html>
					<head>
						<title>Test!</title>
					</head>
					
					<body>
						<h1>Test!</h1>
						<script type="text/javascript">
								var ws = new WebSocket("ws://172.20.0.110:8000/ws");  
	ws.onopen = function() {  
	  ws.send("Hello Mr. Server!");  
	};  
	ws.onmessage = function (e) { alert(e.data); };  
	ws.onclose = function() { };  
						
						</script>
						
					</body>
				</html>
			
			
			"""
			
			start_response(homepage)
	
	s = pywsgi.WSGIServer(("", 8000), request_handler, handler_class=WebSocketHandler)
	s.serve_forever()
	

if __name__ == "__main__":
	main(None)
