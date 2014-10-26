import pygame

from constants import *

class GameScreen(object):

	def __init__(self):
		# initial drawing of game screen
		self.screen = pygame.display.set_mode((1280, 832))
		self.font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 20)
		self.bg = pygame.image.load(IMG_DIR + 'background.png')
		self.player_blit = pygame.image.load(IMG_DIR + 'dude.png')
		self.selection_blit = pygame.image.load(IMG_DIR + 'selection.png')
		self.screen.blit(self.bg, (0, 0))
		self.inventory_screen = self.small_font.render('Inventory', True, WHITE, BLACK)
		self.equipment_screen = self.small_font.render('Equipment', True, WHITE, BLACK)
		self.draw_alert('Welcome to Rougelick!')
		self.stats_screen = self.small_font.render('ARGH', True, WHITE, BLACK)
		self.draw_inventory()
		self.draw_equipment()
		pygame.display.flip()

	def draw_player(self, coord):
		# draws player at specific coordinate
		self.screen.blit(self.player_blit, coord)

	def draw_stats(self, player_stats, color=WHITE):
		# renders player stats
		self.screen.blit(self.stats_screen, (1008, 0))
		self.stats_screen = self.small_font.render(player_stats.name, True, color, BLACK)
		self.screen.blit(self.stats_screen, (1008, 0))
		self.stats_screen = self.small_font.render('Level: {}'.format(player_stats.level), True, color, BLACK)
		self.screen.blit(self.stats_screen, (1008, 15))
		self.stats_screen = self.small_font.render('HP: {}/{}'.format((player_stats.current_hp), (player_stats.max_hp)), True, color, BLACK)
		self.screen.blit(self.stats_screen, (1008, 30))
		line = 45
		for stat in STATS:
			if hasattr(player_stats, stat):
				s = str(getattr(player_stats, stat))
			else:
				s = str(player_stats.stats[stat])
			self.stats_screen = self.small_font.render('{}: {}'.format(stat, s), True, color, BLACK)
			self.screen.blit(self.stats_screen, (1008, line))
			line += 15
		self.stats_screen = self.small_font.render('Armor: {}'.format(player_stats.armor()), True, color, BLACK)
		self.screen.blit(self.stats_screen, (1008, line))
		line += 15

	def draw_treasure(self, treasure_map):
		# draws treasure chests to map
		for row in range(ROWS):
			for col in range(COLUMNS):
				if treasure_map[row][col] != 0:
					treasure = pygame.image.load(IMG_DIR + 'chest.png')
					self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_monsters(self, map):
		for row in range(ROWS):
			for col in range(COLUMNS):
				if map.monsters[row][col] != 0:
					monster = pygame.image.load(IMG_DIR + 'slime.png')
					self.screen.blit(monster, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_walls(self, walls, filename):
		# draws walls on map
		for row in range(ROWS):
			for col in range(COLUMNS):
				if walls[row][col] != 0:
					wall = pygame.image.load(IMG_DIR + filename)
					self.screen.blit(wall, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_darkness(self, map):
		# draws darkness and shadows. 0 is full dark, 1 is shadows, 2 is full reveal
		for row in range(ROWS):
			for col in range(COLUMNS):
				if map.cleared[row][col] == 0:
					if not map.current[row][col]:
						pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE))
				if map.cleared[row][col] == 1:
					if not map.current[row][col]:
						shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
						shadow.set_alpha(200)
						shadow.fill(BLACK)
						self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_background(self):
		self.screen.blit(self.bg, (0, 0))

	def draw_screen_layers(self, map, player_stats):
		# draws layers of game screen
		self.map = map
		self.draw_background()
		self.draw_walls(map.floor, 'floor.png')
		self.draw_walls(map.walls, 'wall.png')
		self.draw_treasure(map.treasure)
		self.draw_monsters(map)
		self.draw_darkness(map)
		self.draw_stats(player_stats=player_stats)
		self.draw_player(coord=map.player)
		self.draw_selection_square()
		self.draw_selected_square_info(map)
		pygame.display.flip()

	def draw_alert(self, alert, color=WHITE):
		# draws alert box at bottom
		self.alert = self.font.render(LONG_STRING, True, BLACK, BLACK)
		self.screen.blit(self.alert, (0, 790))
		try:
			pygame.display.flip()
		except:
			pass
		self.alert = self.font.render(alert, True, color, BLACK)
		self.screen.blit(self.alert, (0, 790))
		pygame.display.flip

	def draw_inventory(self, inventory=None):
		# renders inventory
		self.screen.blit(self.inventory_screen, (1008, 400))
		if inventory:
			items = inventory.get_items()
		else:
			items = []
		for i in range(items.__len__()):
			line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
			self.screen.blit(line, (1008, ((i+1)*15)+400))
		pygame.display.flip()
		for item in items:
			line = self.small_font.render(item.title, True, WHITE, BLACK)
			self.screen.blit(line, (1008, (items.index(item)+1)*15+400))

	def draw_equipment(self, equipment=START_EQUIPMENT):
		# renders equipment. will change for more awesomeness
		self.screen.blit(self.equipment_screen, (1008, 200))
		for i in range(equipment.keys().__len__()):
			line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
			self.screen.blit(line, (1008, ((i+1)*15)+200))
		pygame.display.flip()
		i = 1
		for slot in EQUIPMENT_TYPES:
			try:
				line_text = slot+':   '+equipment[slot].title
			except:
				line_text = slot+':   '
			line = self.small_font.render(line_text, True, WHITE, BLACK)
			self.screen.blit(line, (1008, i*15+200))
			i += 1
		pygame.display.flip()

	def draw_selection_square(self):
		# draw selection square at current mouse position
		mouse_pos = pygame.mouse.get_pos()
		self.selected_tile = [c/TILE_SIZE for c in mouse_pos]
		selection_pos = [c*TILE_SIZE for c in self.selected_tile]
		x, y = self.selected_tile
		try:
			if self.map.floor[x][y] or self.map.walls[x][y]:
				self.screen.blit(self.selection_blit, selection_pos)
		except IndexError:
				# mouse off map
				pass

	def draw_selected_square_info(self, map):
		# draw info regarding contents of currently selected square
		x, y = self.selected_tile
		try:
			if map.monsters[x][y]:
				self.stats_screen = self.small_font.render(str(map.monsters[x][y]), True, (0, 255, 0, 255))
				self.screen.blit(self.stats_screen, (0, 0))
		except IndexError:
			# mouse off map
			pass
