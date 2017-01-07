# create game profile
# game profile:
# min_players
# max_players
# player_age
# category
# mechanic
# min playing time
# max playing time
# expansion
# expands
# publisher
# designer

class GameProfile:

	def __init__(self, min_players, max_players, player_age, categories, \
				mechanics, min_playing_time, max_playing_time, expansion=False, \
				expands="", publishers="", designers=""):
		self.min_players = min_players
		self.max_players = max_players
		self.player_age = player_age
		self.categories = categories
		self.mechanics = mechanics
		self.min_playing_time = min_playing_time
		self.max_playing_time = max_playing_time
		self.expansion = expansion
		self.expands = expands
		self.publishers = publishers
		self.designers = designers

	def printList(self, listOfItems):
		items = ""
		
		for item in listOfItems:
			items += item + "; "

		return items[:-2]

	def displayGameProfile(self):
		print "Game Profile:"
		print "Minimum players: " + str(self.min_players)
		print "Maximum players: " + str(self.max_players)
		print "Player Age: " + str(self.player_age)
		print "Categories: " + self.printList(self.categories)
		print "Mechanics: " + self.printList(self.mechanics)
		print "Minimum playing time: " + str(self.min_playing_time)
		print "Maximum playing time: " + str(self.max_playing_time)
		print "Expansion: " + str(self.expansion)
		print "Expands: " + self.expands
		print "Publishers: " + self.printList(self.publishers)
		print "Designers: " + self.printList(self.designers)

