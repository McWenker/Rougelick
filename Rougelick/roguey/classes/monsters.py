import pygame, math, sys, random
from pygame.locals import *
from constants import *

class Monster(object):
	def __init__(self):
		pass

	@property
	def attack(self):
		return self.stats['Attack']

	def receive_damage(self, damage):
		self.current_hp -= damage

	@property
	def EXP_reward(self):
		return self.stats['EXP']

	@property
	def defense(self):
		return self.stats['Defense']

	@property
	def strength(self):
		return self.stats['Strength']

	def __str__(self):
		return ('{0} | Level {1} | HP {2}/{3} | Attack {4} | Defense {5} | Strength {6} | Agility {7} | Intellect {8}'.format(
					self.title,
					self.level,
					self.current_hp,
					self.max_hp,
					self.stats['Attack'],
					self.stats['Defense'],
					self.stats['Strength'],
					self.stats['Agility'],
					self.stats['Intellect']
					)
				)

class Derpy(Monster):
	def __init__(self):
		self.title = 'Derpy Slime'
		self.level = 1
		self.stats = {
			'Attack': 5,
			'Defense': 1,
			'Strength': 1,
			'Agility': 0,
			'Intellect': 0,
			'EXP': 50,
			'Death Note': (SFX_DIR + 'Acid Bubble.wav')
		}
		self.current_hp = 3
		self.max_hp = 3
		if self.current_hp <= 0:
			self.death_note(self.stats['Death Note'])

class RatBird(Monster):
	def __init__(self):
		self.title = 'Ratbird'
		self.level = 2
		self.stats = {
			'Attack': 7,
			'Defense': 2,
			'Strength': 2,
			'Agility': 4,
			'Intellect': 1,
			'EXP': 150,
			'Death Note': (SFX_DIR + 'Acid Bubble.wav')
		}
		self.max_hp = 5
		self.current_hp = self.max_hp