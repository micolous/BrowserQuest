#!/usr/bin/env python
import server.python.websockets

# wrap the websockets handlers on to a master class
server = server.python.websockets.Server()
web_socket_do_extra_handshake = server.do_extra_handshake
web_socket_transfer_data = server.transfer_data
