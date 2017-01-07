from boardgamegeek import BoardGameGeek
from boardgamegeek import BoardGameGeekAPIError
from boardgamegeek import BoardGameGeekError
import MySQLdb
import unicodedata

db = MySQLdb.connect("localhost", "root", "mouse", "boardgamegeek")
cur = db.cursor()

bgg = BoardGameGeek()

for i in range(3227, 3500):
  try:
	  g = bgg.game(game_id = i)

	  print "id: " + str(g.id)
	  print "name: " + g.name
	  print "description: " + g.description[:1499].replace("&", "and")
	  print "expansion: " + str(g.expansion)
	  print "min players: " + str(g.min_players)
	  print "max players: " + str(g.max_players)
	  print "min age: " + str(g.min_age)
	  print "playing time: " + str(g.playing_time)
	  print "expands: " + str(g.expands)
	  print "average rating: " + str(g.rating_average)

	  bgquery = "insert into boardgame (boardgame_id, name, description, expansion, min_players, "\
	  			"max_players, min_age, playing_time, average_rating) " \
	  			"values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

	  cur.execute(bgquery, (str(g.id), g.name.encode("ascii", "ignore"), unicodedata.normalize('NFKD', g.description[:1495]).encode('ascii', 'ignore'), \
	  			 ('1' if g.expansion else '0'), str(g.min_players), str(g.max_players), str(g.min_age), str(g.playing_time), \
	  			 str(g.rating_average)))

	  print "categories:"

	  for game in g.expands:
	  	print game
	  	expandsquery = "insert into boardgame_expands (boardgame_id, expands_boardgame_id) " \
	  			"values (%s, %s);"
	  	cur.execute(expandsquery, (str(g.id), game.id))

	  print "categories:"

	  for category in g.categories:
	  	print category
	  	categoryquery = "insert into boardgame_category (boardgame_id, category) " \
	  			"values (%s, %s);"
	  	cur.execute(categoryquery, (str(g.id), category))

	  print "mechanics:"

	  for mechanics in g.mechanics:
	  	print mechanics
	  	mechanicsquery = "insert into boardgame_mechanics (boardgame_id, mechanics) " \
	  			"values (%s, %s);"
	  	cur.execute(mechanicsquery, (str(g.id), mechanics))

	  print "designers:"

	  for designer in g.designers:
	    designerquery = "insert into boardgame_designer (boardgame_id, designer) " \
	  			"values (%s, %s);"
	    cur.execute(designerquery, (str(g.id), designer))

	  print "publishers:"

	  for publisher in g.publishers:
	  	print publisher
	  	publisherquery = "insert ignore into boardgame_publisher (boardgame_id, publisher) " \
	  			"values (%s, %s);"
	  	cur.execute(publisherquery, (str(g.id), publisher.encode("ascii", "ignore")))

	  print "expansions:"

	  for expansion in g.expansions:
	  	print expansion
	  	expansionquery = "insert into boardgame_expansion (boardgame_id, expansion_id) " \
	  			"values (%s, %s);"
	  	cur.execute(expansionquery, (str(g.id), expansion.id))

	  db.commit()
  except BoardGameGeekAPIError:
    print("Oops!  BGG formatted the game with id " + str(i) + " incorrectly. Helaas Pindakaas.")
  except BoardGameGeekError:
    print("Oops!  This is not a board game... Helaas Pindakaas.")	


db.close()

