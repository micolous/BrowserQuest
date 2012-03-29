#!/usr/bin/env python
from random import randint

def damage(weapon_level, armor_level):
	dealt = weapon_level * randint(5, 10)
	absorbed = armor_level * randint(1, 3)
	dmg = dealt - absorbed
	
	if dmg <= 0:
		return randint(0, 3)
	else:
		return dmg

def hp(armor_level):
	return 80 + ((armor_level - 1) * 30)
