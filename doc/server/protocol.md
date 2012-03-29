# Protocol Documentation #

Game message types are contained in `shared/js/gametypes.js`.  This contains a large JSON-like object.

More message types are definied in `server/js/message.js`.  This defines the format of the various parameters to messages.

Messages are passed as objects into BiSON format (or JSON, if the server and client are in JSON-mode).  (BiSON.js can be found here)[https://github.com/BonsaiDen/BiSON.js], not to be confused with the much older and widely used language parser (GNU Bison)[http://www.gnu.org/software/bison/].

`server/js/worldserver.js` contains the main gameserver class.

When connecting, a `onPlayerEnter` is called.  This sends a message containing the population to the client.  It will then push an entity list.
