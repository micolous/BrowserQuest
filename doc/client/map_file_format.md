Map File Format
===============

**Map JSON has the following keys:**

##animated

An array of tile indeces in `data` of tiles that are animated

##blocking

An array of tile indeces in `data` of tiles that are non-walkable

##checkpoints

##collisions

An array of tile indeces in `data` of tiles that produce a collision

##data

The big one: an array with length `height * width`, a tileID to represent each worldmap tile.  Tile [0,0] is in the upper left corner of the worldmap

##doors

##height

The height of the worldmap in tiles

##high

##musicAreas

##plateau

##tilesize

##width 

The width of the worldmap in tiles