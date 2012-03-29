# Protocol Documentation #

Game message types are contained in `shared/js/gametypes.js`.  This contains a large JSON-like object.

More message types are definied in `server/js/message.js`.  This defines the format of the various parameters to messages.

Messages are passed as objects into BiSON format (or JSON, if the server and client are in JSON-mode).  (BiSON.js can be found here)[https://github.com/BonsaiDen/BiSON.js], not to be confused with the much older and widely used language parser (GNU Bison)[http://www.gnu.org/software/bison/].

`server/js/worldserver.js` contains the main gameserver class.

When connecting, a `onPlayerEnter` is called.  This sends a message containing the population to the client.  It will then push an entity list.


## Connection ##

On connection, the server should send the message "go" to the client.

This will then trigger the client to start using it's JSON protocol.  Messages are transmitted as JSON arrays, with the zeroth element being a message ID.  The following message types are used by the server:

### HELLO (0) (C -> S) ###

This is the first message the client sends when logging in.  This command should not be repeated.  No other commands will be accepted before the client sends this.

1. Player name (string), limit 16 characters.
2. Armor type (int)
3. Weapon type (int)

### WELCOME (1) ###