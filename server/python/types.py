#!/usr/bin/env python
"""
Datatypes defined for client-server communications.

Welcome to the only file that is actually shared between the client and the 
server, and the NodeJS hipster's way of saying "you should totally write your
server side code in JavaScript because you can share code!!11one".

Yup, it's a fucking joke, and a lie.  There is almost no code shared in this,
despite Mozilla's PR, and plenty of opportunity for code reuse.

In the end you're stuck with the trainwreck that is NodeJS, and it's totally
not worth it at all.

"""
ORIENTATIONS = dict(
	UP = 1,
	DOWN = 2,
	LEFT = 3,
	RIGHT = 4
)

ENTITIES = dict(
	WARRIOR = 1,

	# Mobs
	RAT = 2,
	SKELETON = 3,
	GOBLIN = 4,
	OGRE = 5,
	SPECTRE = 6,
	CRAB = 7,
	BAT = 8,
	WIZARD = 9,
	EYE = 10,
	SNAKE = 11,
	SKELETON2 = 12,
	BOSS = 13,
	DEATHKNIGHT = 14,

	# Armors
	FIREFOX = 20,
	CLOTHARMOR = 21,
	LEATHERARMOR = 22,
	MAILARMOR = 23,
	PLATEARMOR = 24,
	REDARMOR = 25,
	GOLDENARMOR = 26,

	# Objects
	FLASK = 35,
	BURGER = 36,
	CHEST = 37,
	FIREPOTION = 38,
	CAKE = 39,

	# NPCs
	GUARD = 40,
	KING = 41,
	OCTOCAT = 42,
	VILLAGEGIRL = 43,
	VILLAGER = 44,
	PRIEST = 45,
	SCIENTIST = 46,
	AGENT = 47,
	RICK = 48,
	NYAN = 49,
	SORCERER = 50,
	BEACHNPC = 51,
	FORESTNPC = 52,
	DESERTNPC = 53,
	LAVANPC = 54,
	CODER = 55,

	# Weapons
	SWORD1 = 60,
	SWORD2 = 61,
	REDSWORD = 62,
	GOLDENSWORD = 63,
	MORNINGSTAR = 64,
	AXE = 65,
	BLUESWORD = 66
)


def get_orientation_as_string(orientation):
	if orientation == ORIENTATIONS['UP']:
		return 'up'
	elif orientation == ORIENTATIONS['DOWN']:
		return 'down'
	elif orientation == ORIENTATIONS['LEFT']:
		return 'left'
	elif orientation == ORIENTATIONS['RIGHT']:
		return 'right'
	else:
		raise ValueError, "Orientation numeric is invalid."

def is_player(kind):
	return ENTITIES['WARRIOR'] == kind

def is_mob(kind):
	return ENTITIES['RAT'] <= kind <= ENTITIES['DEATHKNIGHT']

def is_npc(kind):
	return ENTITIES['GUARD'] <= kind <= ENTITIES['CODER']

def is_character(kind):
	return is_mob(kind) or is_npc(kind) or is_player(kind)

def is_armor(kind):
	return ENTITIES['FIREFOX'] <= kind <= ENTITIES['GOLDENARMOR']

def is_weapon(kind):
	return ENTITIES['SWORD1'] <= kind <= ENTITIES['BLUESWORD']

def is_item(kind):
	return is_weapon(kind) or is_armor(kind) or (is_object(kind) and not is_chest(kind))

def is_object(kind):
	return ENTITIES['FLASK'] <= kind <= ENTITIES['CAKE']

def is_chest(kind):
	return ENTITIES['CHEST'] == kind

	