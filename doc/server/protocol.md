# Protocol Documentation #

Game message types are contained in `shared/js/gametypes.js`.  This contains a large JSON-like object.

More message types are definied in `server/js/message.js`, with additional protocol decoding by `server/js/player.js`.  This defines the format of the various parameters to messages.  In the client the messages are encoded and decoded by `client/js/gameclient.js`.

Contrary to Mozilla's announcement of the project, there is very little client and server code shared.  The only shared code is in `shared/js/gametypes.js`, which is a bunch of defines for message types.  None of the message serialisation and deserialisation code is shared.  Several messages are different on client and server side.

Messages are passed as objects into BiSON format (or JSON, if the server and client are in JSON-mode).  [BiSON.js can be found here](https://github.com/BonsaiDen/BiSON.js), not to be confused with the much older and widely used language parser [GNU Bison](http://www.gnu.org/software/bison/).

`server/js/worldserver.js` contains the main gameserver class.

When connecting, a `onPlayerEnter` is called.  This sends a message containing the population to the client.  It will then push an entity list.

## Entity Types ##

### Player ###

* `1` Warrior

### Mobs ###

* `2` Rat
* `3` Skeleton
* `4` Goblin
* `5` Ogre
* `6` Spectre
* `7` Crab
* `8` Bat
* `9` Wizard
* `10` Eye
* `11` Snake
* `12` Skeleton (2)
* `13` Boss
* `14` Death Knight

### Armors ###

* `20` Firefox
* `21` Cloth armor
* `22` Leather armor
* `23` Mail (chain) armor
* `24` Plate armor
* `25` Red armor
* `26` Golden armor

### Objects ###

* `35` Flask
* `36` Burger
* `37` Treasure chest
* `38` Fire potion
* `39` Cake

### Non-player characters ###

* `40` Guard
* `41` King
* `42` Octocat (github mascot)
* `43` Female villager
* `44` Male villager
* `45` Priest
* `46` Scientist
* `47` Agent

TODO: finish this list.

## Orientations ##

* `1` Up / north
* `2` Down / south
* `3` Left / west
* `4` Right / east

## Connection ##

On connection, the server should send the message "go" to the client.

This will then trigger the client to start using it's JSON protocol.  Messages are transmitted as JSON arrays, with the zeroth element being a message ID.  The following message types are used by the server:

### HELLO (0) (Client) ###

This is the first message the client sends when logging in.  This command should not be repeated.  No other commands will be accepted before the client sends this.

* `1` Player name (string), limit 16 characters.
* `2` Armor type (int)
* `3` Weapon type (int)

### WELCOME (1) (Server) ###

This is a response to a HELLO command from the client.

* `1` The player's entity ID. (int)
* `2` The sanitised version of the player's name, ie: name size limited to 16 characters, SGML/XML characters removed. (string)
* `3` The player's X co-ordinate on the map. (int)
* `4` The player's Y co-ordinate on the map. (int)
* `5` The number of hit points the player has. (int)

## Game play ##

One HELLO/WELCOME packets have been exchanged, the main game packets can be sent.

### SPAWN (2) (Server) ###

Spawns an Entity in the game.

* `1` The entity ID. (int)
* `2` The entity kind ID.  See `Entity Types`. (int)
* `3` The X co-ordinate of the entity on the map. (int)
* `4` The Y co-ordinate of the entity on the map. (int)

If the entity is a Player, the additional parameters are supplied:

* `5` The player's name. (string)
* `6` The orientation of the player. (int)
* `7` The player's armor kind. (int)
* `8` The player's weapon kind. (int)

### DESPAWN (3) (Server) ###

Removes an Entity from the game.

* `1` The entity ID. (int)

### MOVE (4) (Server, Client) ###

From the client, this moves the player to the location given.

From the server, this moves any entity to the location given.

This has been changed in my branch of the code.   The original version sent Client -> Server messages with the following format:

* `1` X-position of the player. (int)
* `2` Y-position of the player. (int)

My version changes the Client -> Server packet so that it is the same as the Server -> Client packet:

* `1` The entity ID that is moving.  The server should ignore this value sent by the client. (int)
* `2` X-position of the entity / player. (int)
* `3` Y-position of the entity / player. (int)

### CHAT (11) (Server, Client) ###

This has been changed in my branch of the code.  The original version sent Client -> Server messages with the following format:

* `1` The message that the client wishes to send. (int)

My version changes the Client -> Server packet so that it is the same as the Server -> Client packet:

* `1` The entity ID that wishes to talk.  The server should ignore this value sent by the client. (int)
* `2` The message that the entity wishes to send / has sent.
