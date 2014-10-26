from player import Player
from monsters import Derpy
import pygame
from constants import *

from random import randint

class Combat(object):
	
	def __init__(self, player, monster):
		self.player = player
		self.monster = monster
		self.attack_sound = pygame.mixer.Sound(SFX_DIR + 'Sword.wav')
		self.fight()
		
	def fight(self):
		# for now, always start with player
		# player hits monster
		self.attack_sound.play()
		hit_attempt = randint(0, self.player.attack)
		if hit_attempt > self.monster.defense:
			damage = self.player.attack
			self.monster.receive_damage(damage)

		# monster hits back
		if self.monster.current_hp > 0:
			hit_attempt = randint(0, self.monster.attack)
			if hit_attempt > self.player.defense:
				damage = self.monster.strength
				self.player.receive_damage(damage)

	def award_exp(self):
		self.player.stats['EXP'] += self.monster.stats['EXP']

	def death_note(self, filename):
		self.death = pygame.mixer.Sound(filename)
		self.death.play()