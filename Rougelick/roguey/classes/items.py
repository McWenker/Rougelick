import pygame, math, sys, random, pickle
from pygame.locals import *

from constants import *

class Treasure(object):
	def __init__(self, title='Nada', description='', item_type='trash', armor=0, buff=0, attack=0):
		self.title = title
		self.description = description
		self.item_type = item_type
		self.armor = armor
		self.buff = buff
		self.attack = attack