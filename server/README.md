# BrowserQuest server documentation #

## `node.js` version (original) ##

The game server currently runs on nodejs v0.4.7 (but should run fine on the latest stable as well) and requires the latest versions of the following npm libraries:

- underscore
- log
- bison
- websocket
- websocket-server
- sanitizer
- memcache (only if you want metrics)

All of them can be installed via `npm install -d` (this will install a local copy of all the dependencies in the node_modules directory)


### Configuration ###

The server settings (number of worlds, number of players per world, etc.) can be configured.
Copy `config_local.json-dist` to a new `config_local.json` file, then edit it. The server will override default settings with this file.


### Deployment ###

In order to deploy the server, simply copy the `server` and `shared` directories to the staging/production server.

Then run `node server/js/main.js` in order to start the server.


Note: the `shared` directory is the only one in the project which is a server dependency.


### Monitoring ###

The server has a status URL which can be used as a health check or simply as a way to monitor player population.

Send a GET request to: `http://[host]:[port]/status`

It will return a JSON array containing the number of players in all instanced worlds on this game server.


## Python version (in development) ##

The game server is still in development.  Currently using:

- mod_pywebsocket

It can be installed via `pip install [module_name]`.  Python 2.6 or later is required.  Python 3 is not supported at this time.

The goal is to be 100% compatible with the original JavaScript version of the server, including worlds and configuration files.

This is currently not complete, only the client loads, there is no server to connect to yet.

### Deployment ###

It may be possible to load this inside of `mod_pywebsockets` with a working Apache server.  Otherwise included in the root directory of the project is a `run_server` shell (sh) and Windows command script (cmd).

Running the appropriate one for your platform will start up a development server with the client hosted at port 8000.  To use it, visit http://localhost:8000/client/

There's currently a bug in the websockets handler taking over / for non-WebSockets requests.

Don't forget to update /client/config/config_build.json with your server settings, if you're running it on something other than localhost.