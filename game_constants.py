from enum import Enum
from dataclasses import dataclass
from typing import Tuple

MAX_OBSTACLE_NUMBER = 15
MIN_OBSTACLE_NUMBER = 1
GRID_LETTERS = ("A", "B", "C", "D", "E", "F", "G")

class Names(object):
	GREEN_SQUAD = "Forest defenders"
	PURPLE_SQUAD = "Night warriors"
	GREEN_SQUAD_CHARACTERS = ("Ivy assassin", "Spruce archer", "Moss druid")
	PURPLE_SQUAD_CHARACTERS = ("Dark thief", "Black hunter", "Void sorcerer")

class CharacterTypes(Enum):
	rogue = 1
	ranger = 2
	mage = 3

@dataclass
class SquadInfo:
	name: str
	names: Tuple[str, str, str]
	sprites: Tuple[str, str, str]
	types: Tuple[CharacterTypes, CharacterTypes, CharacterTypes]
