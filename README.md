BrowserQuest
============

Documentation is located in client and server directories.

## About this fork (micolous/BrowserQuest) ##

Because there seems to be rather a lot of forks of this project, I should describe mine!

My fork has three main goals at this time:

 1. Port the server to Python.
   
    I've mostly ported the code directly for this preferring to keep close to the JavaScript implementation.  There's some changes that I've made to the layout in the Python version to make things cleaner.
    
 2. Improve technical documentation of the client-server protocol, and static file formats.
    
    Through development of the Python protocol I've written a bunch of documentation on how it works.  Hopefully this will be useful for future porting efforts.
    
 3. Improve the protocol such that the client/server protocol is a little bit more consistant. 
    
    I've also ported back those protocol changes to the Javascript client/server, as well as documented the difference between my version of the protocol and the mainline version of the protocol.
    
    However, be warned my changes to the JavaScript version of the server are **completely** untested.  I refuse to install node.js on any of my computers.  If you do install node.js on your computer and find such bugs, I'll happily take patches.  As a result I've made any changes to the protocol as minor as possible.
