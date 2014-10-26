from constants import *
import operator

class Inventory(object):
	# player inventory

	def __init__(self):
		# setups initial blank inventory
		self.inventory = {}

	def get_items(self):
		return self.inventory.keys()

	def add_to_inventory(self, item, player):
		# adds item to inventory
		if item.item_type == 'trash':
			return
		if player.equipped[item.item_type]:
			try:
				self.inventory[item] += 1
			except:
				self.inventory[item] = 1
		else:
			player.equip_item(item)

class Player(object):
	# player class, contains stats and deals with combat
	def __init__(self):
		self.level = 1
		self.stats = {
			'Strength': 1,
			'Attack': 5,
			'Defense': 5,
			'Agility': 1,
			'Intellect': 1,
			'EXP': 0
		}
		self.class_type = {
			'Warrior': 0,
			'Archer': 0,
			'Wizard': 0
		}
		self.current_hp = 10
		self.main_stat = self.find_main_stat(self.class_type)
		self.name = 'Rougelicker'
		self.equipped = {}

		for treasure in EQUIPMENT_TYPES:
			self.equipped[treasure] = None

	@property
	def max_hp(self):
		return (10 + ((self.level-1)*5) + (self.class_type['Warrior']*5))

	@property
	def max_mp(self):
		return (0 + (self.class_type['Wizard']*10))

	@property
	def defense(self):
		return (self.stats['Defense'] + self.armor() + self.class_type['Archer'])

	@property
	def strength(self):
		return (self.stats['Strength'] + (self.class_type['Warrior']*2))

	@property
	def agility(self):
		return (self.stats['Agility'] + (self.class_type['Archer']*2))

	@property
	def intellect(self):
		return (self.stats['Intellect'] + (self.class_type['Wizard']*2))

	@property
	def EXP(self):
		return self.stats['EXP']

	def armor(self):
		armor = 0
		for slot in self.equipped.keys():
			if self.equipped[slot]:
				try:
					armor += self.equipped[slot].armor
				except AttributeError:
					pass
		return armor

	def receive_damage(self, damage):
		self.current_hp -= damage

	def attempt_block(self, attack):
		pass

	@property
	def attack(self):
		if self.stats[self.main_stat]:
			atk = (0 + self.stats[self.main_stat])
		else:
			# no class levels!
			atk = 0
		if self.equipped['weapon']:
			try:
				atk += self.equipped['weapon'].damage
			except AttributeError:
				# this weapon does not have a 'damage' attribute
				pass
		return self.stats['Attack']+atk

	def equip_item(self, item):
		self.equipped[item.item_type] = item

	def find_main_stat(self, _list):
		# reads list of invested level-ups, chooses main stat based on class
		# if level 1, returns None

		index = sorted(_list.values())[0]
		if index == 'Warrior':
			return 'Strength'
		elif index == 'Archer':
			return 'Agility'
		elif index == 'Wizard':
			return 'Intellect'
		else:
			return 'Strength'