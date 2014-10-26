import sys, pickle

sys.path.append("roguey/classes")

from items import Treasure
from constants import *


class Admin(object):
	def __init__(self):
		f = open("roguey/resources/items.pk")
		try:
			self.treasures = pickle.load(f)
		except:
			print "No treasures!"
			self.treasures = []
		f.close()
		self.main()

	def new_treasure(self):
		for treasure in TREASURE_TYPES:
			print "%s. %s" % (TREASURE_TYPES.index(treasure)+1, treasure)
		choice = raw_input("\nPick a type [1-9]: ")
		item_type = TREASURE_TYPES[int(choice)-1]
		title = raw_input("Give it a title: ")
		desc = raw_input("Give it a description: ")
		armor = int(raw_input("\nAdd armor? [#]: "))
		attack = int(raw_input("\nAdd attack? [#]: "))
		tr = Treasure(title=title, description=desc, item_type=item_type, armor=armor, attack=attack)
		self.treasures.append(tr)

	def list_treasures(self):
		print "Current treasures:\n"
		for index, treasure in enumerate(self.treasures):
			print index, treasure.title
			print '   "{}"'.format(treasure.description)
			print "   ({})".format(treasure.item_type)
			if treasure.armor:
				print "   +{} armor".format(treasure.armor)
			if treasure.attack:
				print "   +{} attack".format(treasure.attack)
		print "\n"

	def save(self):
		f = open("roguey/resources/items.pk", "w")
		pickle.dump(self.treasures, f)
		f.close()

	def del_treasure(self):
		self.list_treasures()
		d = int(raw_input("Choose treasure to remove: "))
		print "\n{} has been removed.".format(self.treasures[d].title)
		del self.treasures[d]

	def yes_no(self, prompt):
		# prompt for a yes/no answer
		# will accept anything beginning with Y, N, y, or n
		# returns bool
		retval = None
		selection = raw_input('%s (Y/N): ' % prompt)
		# continue to prompt until valid input
		while retval == None:
			first_letter = selection.strip()[0].upper()
			try:
				retval = {
					"Y": True,
					"N": False
				}
			except KeyError:
				pass
		return retval

	def main(self):
		c = None
		while 1:
			print "\n**************************"
			print "\n1. Make a new treasure"
			print "2. List current treasures"
			print "3. Delete a treasure"
			print "0. Quit"
			print "\n**************************\n"
			c = raw_input("Make a choice [1-3, 0]: ")
			if c[0] == "1": self.new_treasure()
			if c[0] == "2": self.list_treasures()
			if c[0] == "3": self.del_treasure()
			if c[0] == "0": 
				self.save()
				return
			try:
				c = int(c)-1
			except ValueError:
				print "Invalid input. [1-3, 0]"
				c = None
				continue
			if c < 0 or c > 3:
				print "Invalid input. [1-3, 0]"
				c = None
				continue

if __name__ == "__main__":
	a = Admin()