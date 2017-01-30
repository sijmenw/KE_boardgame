# create game class
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
# family
# rating

class Game(object):

	def __init__(self, boardgame_id, name, min_players, max_players, player_age, \
				categories, mechanics, description, playing_time, expansion, \
				expands, publishers, designers, rating):
		self.boardgame_id = boardgame_id
		self.name = name
		self.min_players = min_players
		self.max_players = max_players
		self.player_age = player_age
		self.categories = categories
		self.mechanics = mechanics
		self.description = description
		self.playing_time = playing_time
		self.expansion = expansion
		self.expands = expands
		self.publishers = publishers
		self.designers = designers
		self.rating = rating

	def printList(self, listOfItems):
		items = ""
		
		for item in listOfItems:
			items += item + "; "

		return items[:-2]

	def displayGame(self):
		print "Game Profile:"
		print "ID: " + str(self.boardgame_id)
		print "Name: " + self.name
		print "Minimum players: " + str(self.min_players)
		print "Maximum players: " + str(self.max_players)
		print "Player Age: " + str(self.player_age)
		print "Categories: " + self.printList(self.categories)
		print "Mechanics: " + self.printList(self.mechanics)
		print "Description: " + self.description
		print "Playing time: " + str(self.playing_time)
		print "Expansion: " + str(self.expansion)
		print "Expands: " + self.expands
		print "Publishers: " + self.printList(self.publishers)
		print "Designers: " + self.printList(self.designers)
		print "Rating: " + str(self.rating)



