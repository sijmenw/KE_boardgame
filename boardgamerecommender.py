from gameprofile import GameProfile
from game import Game
import MySQLdb
import credentials

#WHILE NEW-SOLUTION generate(object -> class) DO
# candidate-classes := class ADD candidate-classes;
#END WHILE

def generateCandidateGames():

    db = credentials.connect()
    cur = db.cursor()

    #get each candidate from the 'boardgame' table
    canditatesQuery = "select * from boardgame;"

    try:
        cur.execute(canditatesQuery)
        gameResults = cur.fetchall()

        games = []

        for game in gameResults:
            boardgame_id = game[0]
            name = game[1]
            description = game[2]
            expansion = game[3]
            min_players = game[4]
            max_players = game[5]
            min_age = game[6]
            playing_time = game[7]
            rating = game[8]

            #get all multiple values for each candidate: categories, mechanics, publishers and designers
            categoriesQuery = "select category from boardgame_category where boardgame_id = " + str(boardgame_id) + ";"
            mechanicsQuery = "select mechanics from boardgame_mechanics where boardgame_id = " + str(boardgame_id) + ";"
            publishersQuery = "select publisher from boardgame_publisher where boardgame_id = " + str(boardgame_id) + ";"
            designersQuery = "select designer from boardgame_designer where boardgame_id = " + str(boardgame_id) + ";"

            categories = getMultipleAttributeValues(cur, categoriesQuery)
            mechanics = getMultipleAttributeValues(cur, mechanicsQuery)
            publishers = getMultipleAttributeValues(cur, publishersQuery)
            designers = getMultipleAttributeValues(cur, designersQuery)

            game = Game(boardgame_id, name, min_players, max_players, min_age, categories, \
                        mechanics, description, playing_time, False, "test", publishers, \
                        designers, rating)

            games.append(game)
    except:
        print "Error: unable to fetch data"

    db.close()
    return games

#WHILE NEW-SOLUTION specify(candidate-classes -> attribute)
#       AND SIZE candidate-classes > 1 DO
#     obtain(attribute -> new-feature);
#     current-feature-set := new-feature ADD current-feature-set;
#     FOR-EACH class IN candidate-classes DO
#       match(class + current-feature-set -> truth-value);
#     IF truth-value == false
#     THEN
#       candidate-classes := candidate-classes SUBTRACT class;
#     END IF
#   END FOR-EACH

def obtainRecommendations(gameProfile, games):
    recommendations = []

    for game in games:
        if matchFeatureSet(gameProfile, game):
            print game.name
            recommendations.append(game) 

#check if there is an overlap between features that allow multiple values
def matchList(gameProfileFeatures, gameFeatures):
    return len(list(set(gameProfileFeatures) & set(gameFeatures))) > 0

def matchFeatureSet(gameProfile, game):

    return (game.min_players >= gameProfile.min_players and 
            game.max_players <= gameProfile.max_players and
            game.player_age >= gameProfile.player_age and 
            game.playing_time >= gameProfile.min_playing_time and 
            game.playing_time <= gameProfile.max_playing_time and 
            matchList(game.categories, gameProfile.categories) and 
            matchList(game.mechanics, gameProfile.mechanics))


def getMultipleAttributeValues(cur, query):
    cur.execute(query)
    attrValues = cur.fetchall()

    valueList = []

    for value in attrValues:
        valueList.append(value[0])

    return valueList

def build_profile(dict):
    profile = GameProfile(dict["min_players"], dict["max_players"], dict["player_age"], )

    return profile

def main():
    gp = GameProfile(2, 6, 10, ["Economic"], ["Area Control / Area Influence", "Tile Placement", "Dice Rolling"], 5, 240)

    gp.displayGameProfile()

    games = generateCandidateGames()

    obtainRecommendations(gp, games)

if __name__ == "__main__":
    main()