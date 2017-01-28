# all the imports
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from gameprofile import GameProfile
from game import Game
import MySQLdb
import credentials

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    return app.send_static_file('client.html')


@app.route('/query_games/', methods=['POST'])
def query_games():
    # get data
    dict_input = request.get_json(force=True)

    recommendations = recommend(dict_input)

    print recommendations

    result = {'success': 'true', 'message': 'Heuy fissa', 'data': [ob.__dict__ for ob in recommendations]}
    return json.dumps(result)


@app.route('/get_form_options/', methods=['POST'])
def get_form_options():

    categoriesQuery = "select distinct category from boardgame_category;"
    mechanicsQuery = "select distinct mechanics from boardgame_mechanics;"

    categories_list = getDistinctOptions(categoriesQuery)
    mechanics_list = getDistinctOptions(mechanicsQuery)

    checkboxes = {'categories': categories_list, 'mechanics': mechanics_list}

    result = {'success': 'true', 'message': 'Here are the dropdowns', 'data': checkboxes}
    return json.dumps(result)

def getDistinctOptions(query):
    result_list = []

    try:
        db = credentials.connect()
        cur = db.cursor()
        cur.execute(query)
        results = cur.fetchall()

        for res in results:
            result_list.append(res[0])
    except Exception as e:
        print "Error: unable to fetch data" + str(e)
        db.close()

    db.close()
    return result_list

#WHILE NEW-SOLUTION generate(object -> class) DO
# candidate-classes := class ADD candidate-classes;
#END WHILE

def generateCandidateGames():

    db = credentials.connect()
    cur = db.cursor()

    #get each candidate from the 'boardgame' table
    canditatesQuery = "select * from boardgame limit 100;"

    try:
        cur.execute(canditatesQuery)
        gameResults = cur.fetchall()

        description = ""
        games = []

        for game in gameResults:
            boardgame_id = game[0]
            name = game[1]
            expansion = game[2]
            min_players = game[3]
            max_players = game[4]
            min_age = game[5]
            playing_time = game[6]
            rating = game[7]

            #get all multiple values for each candidate: categories, mechanics, publishers and designers
            categoriesQuery = "select category from boardgame_category where boardgame_id = " + str(boardgame_id) + ";"
            mechanicsQuery = "select mechanics from boardgame_mechanics where boardgame_id = " + str(boardgame_id) + ";"
            #publishersQuery = "select publisher from boardgame_publisher where boardgame_id = " + str(boardgame_id) + ";"
            #designersQuery = "select designer from boardgame_designer where boardgame_id = " + str(boardgame_id) + ";"

            categories = getMultipleAttributeValues(cur, categoriesQuery)
            mechanics = getMultipleAttributeValues(cur, mechanicsQuery)
            #publishers = getMultipleAttributeValues(cur, publishersQuery)
            #designers = getMultipleAttributeValues(cur, designersQuery)

            game = Game(boardgame_id, name, min_players, max_players, min_age, categories, \
                        mechanics, description, playing_time, False, "test", [], \
                        [], rating)

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
    
    return recommendations

#check if there is an overlap between features that allow multiple values
def matchList(gameProfileFeatures, gameFeatures):
    return len(list(set(gameProfileFeatures) & set(gameFeatures))) > 0


#Knowledge base specified by rule types
#Match inference step
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

def recommend(profparams):
    #print profparams['min_players']
    gp = GameProfile(int(profparams['min_players']), int(profparams['max_players']), 10, ["Economic"], ["Area Control / Area Influence", "Tile Placement", "Dice Rolling"], 5, 240)
    
    gp.displayGameProfile()

    games = generateCandidateGames()

    recommendations = obtainRecommendations(gp, games)

    return recommendations

if __name__ == '__main__':
    app.run()
