import os

MOVEMENT = 12
RADIUS = 2
BLACK = (0,0,0)
WHITE = (255, 255, 255)
COLUMNS = 16
ROWS = 21
TREASURES = 10
MAX_ROOMS = 7
MONSTERS = 12
TILE_SIZE = 48
DIRECTIONS = ['north', 'south', 'east', 'west']
LONG_STRING = 'X' * 50

EQUIPMENT_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon')
START_EQUIPMENT = {}
for treasure in EQUIPMENT_TYPES:
	START_EQUIPMENT[treasure] = None

TREASURE_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon', 'trash')

IMG_DIR = os.getcwd() + '/roguey/images/'
SFX_DIR = os.getcwd() + '/roguey/SFX/'

STATS = ('Strength', 'Attack', 'Defense', 'Agility', 'Intellect', 'EXP')
CLASS = ('Warrior', 'Archer', 'Wizard')