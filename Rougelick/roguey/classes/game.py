import pygame, sys, pickle
from pygame.locals import *

from constants import *
from items import Treasure
from gamemap import Map
from monsters import Derpy
from player import Inventory, Player
from combat import Combat
from gamescreen import GameScreen

class Game(object):
	# game object, controls rendering game and moving player
	def __init__(self):
		self.screen = GameScreen()
		self.bg = pygame.image.load(IMG_DIR + 'background.png')
		death_sound = pygame.mixer.Sound(SFX_DIR + 'death.ogg')
		
		self.inventory = Inventory()
		self.map = Map()
		self.map.player = (1*TILE_SIZE, 1*TILE_SIZE)
		self.player_stats = Player()
		treasure = self.map.clear_treasure(self.map.player)
		if treasure:
			self.add_treasure(treasure)

		self.clock = pygame.time.Clock()
		self.direction = 0

		self.map.clear_block(self.map.player)
		self.map.set_current_position(self.map.player)
		
		self.screen.draw_screen_layers(player_stats=self.player_stats, map=self.map)
		
		self.run()

	def add_treasure(self, treasure):
		text = 'You found a %s. %s' % (treasure.title, treasure.description)
		self.inventory.add_to_inventory(treasure, self.player_stats)
		self.screen.draw_alert(text)

	def move(self, hor, vert):
		# given keypress, moves player
		# also checks for fight or treasure pick-up
		self.old_row, self.old_col = self.map.player
		row = self.old_row + hor
		col = self.old_col + vert
		if row > (ROWS-1)*TILE_SIZE or row < 0 or col > (COLUMNS-1)*TILE_SIZE or col < 0:
			return
		if self.map.has_wall(row, col):
			return
		if self.map.has_monster(row, col):
			Combat(self.player_stats, self.map.monsters[row/TILE_SIZE][col/TILE_SIZE]).fight()
			if self.map.monsters[row/TILE_SIZE][col/TILE_SIZE].current_hp <= 0:
				Combat(self.player_stats, self.map.monsters[row/TILE_SIZE][col/TILE_SIZE]).award_exp()
				Combat(self.player_stats, self.map.monsters[row/TILE_SIZE][col/TILE_SIZE]).death_note(self.map.monsters[row/TILE_SIZE][col/TILE_SIZE].stats['Death Note'])
				self.map.monsters[row/TILE_SIZE][col/TILE_SIZE] = 0
			if self.player_stats.current_hp <= 0:
				death_sound.play()
				self.end_game()
			self.move(0, 0)
			return
		self.map.player = (row, col)
		self.map.player = (row, col)
		self.map.clear_block(self.map.player)
		self.map.set_current_position(self.map.player)
		treasure = self.map.clear_treasure(self.map.player)
		if treasure:
			self.add_treasure(treasure)
			self.screen.draw_inventory(self.inventory)
			self.screen.draw_equipment(self.player_stats.equipped)

	def refresh_screen(self):
		self.screen.draw_player(self.map.player)
		self.screen.draw_screen_layers(self.map, self.player_stats)

	def end_game(self):
		# exit screen for when player has died or won

		self.terminate()

	def run(self):
		# event handler
		hor = 0
		vert = 0
		hard_music = 0
		while hard_music == 0:
			self.begin_music()
			hard_music = 1

		while 1:
			self.clock.tick(30)

			for event in pygame.event.get():
				if not hasattr(event, 'key'):
					continue
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.terminate()
					if event.key == K_LEFT:
						hor = -TILE_SIZE
						vert = 0
					if event.key == K_RIGHT:
						hor = TILE_SIZE
						vert = 0
					if event.key == K_UP:
						vert = -TILE_SIZE
						hor = 0
					if event.key == K_DOWN:
						vert = TILE_SIZE
						hor = 0
				if event.type == KEYUP:
					self.map.move_monsters()
					self.move(hor, vert)
					hor = 0
					vert = 0
			self.refresh_screen()

	def terminate(self):
		pygame.quit()
		sys.exit()

	def begin_music(self):
		pygame.mixer.init(22050, -8, 4, 4096)
		pygame.mixer.music.load(SFX_DIR + 'Raver.flac')
		pygame.mixer.music.play(-1, 0.0)