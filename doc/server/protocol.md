# Protocol Documentation #

Game message types are contained in `shared/js/gametypes.js`.  This contains a large JSON-like object.

More message types are definied in `server/js/message.js`.  This defines the format of the various parameters to messages.

Messages are passed as objects into BiSON format (or JSON, if the server and client are in JSON-mode).  [BiSON.js can be found here](https://github.com/BonsaiDen/BiSON.js), not to be confused with the much older and widely used language parser [GNU Bison](http://www.gnu.org/software/bison/).

`server/js/worldserver.js` contains the main gameserver class.

When connecting, a `onPlayerEnter` is called.  This sends a message containing the population to the client.  It will then push an entity list.


## Connection ##

On connection, the server should send the message "go" to the client.

This will then trigger the client to start using it's JSON protocol.  Messages are transmitted as JSON arrays, with the zeroth element being a message ID.  The following message types are used by the server:

### HELLO (0) (Client) ###

This is the first message the client sends when logging in.  This command should not be repeated.  No other commands will be accepted before the client sends this.

1. Player name (string), limit 16 characters.
2. Armor type (int)
3. Weapon type (int)

### WELCOME (1) (Server)###

This is a response to a HELLO command from the client.

1. The player's entity ID.
2. The sanitised version of the player's name, ie: name size limited to 16 characters, SGML/XML characters removed.
3. The player's X co-ordinate on the map.
4. The player's Y co-ordinate on the map.
5. The number of hit points the player has.
