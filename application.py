# all the imports
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from gameprofile import GameProfile
from game import Game
import MySQLdb
import credentials
from operator import itemgetter

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

    print dict_input

    recommendations = recommend(dict_input)

    resultData = []
    
    for r in recommendations:
        resultData.append(r.__dict__)


    result = {'success': 'true', 'message': 'Heuy fissa', 'data': resultData}
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
    canditatesQuery = "select * from boardgame;"
    categoriesQuery = "select * from boardgame_category";
    mechanicsQuery = "select * from boardgame_mechanics";

    categoriesDict = getMultipleAttributeValues(cur, categoriesQuery)
    mechanicsDict = getMultipleAttributeValues(cur, mechanicsQuery)

    try:
        cur.execute(canditatesQuery)
        gameResults = cur.fetchall()

        description = ""
        games = []
        categories = []
        mechanics = []

        for game in gameResults:
            boardgame_id = game[0]
            name = game[1]
            expansion = game[2]
            min_players = game[3]
            max_players = game[4]
            min_age = game[5]
            playing_time = game[6]
            rating = game[7]

            if boardgame_id in categoriesDict:
                categories = categoriesDict[boardgame_id]

            if boardgame_id in mechanicsDict:
                mechanics = mechanicsDict[boardgame_id]

            game = Game(boardgame_id, name, min_players, max_players, min_age, categories, \
                        mechanics, description, playing_time, False, "test", [], \
                        [], rating)

            games.append(game)
    except Exception as e:
        print "Error: unable to fetch data" + str(e)

    db.close()
    return games

def getMultipleAttributeValues(cur, query):
    cur.execute(query)
    attrValues = cur.fetchall()

    valueList = {}

    for value in attrValues:
        vals = []
        if value[0] not in valueList:
            vals.append(value[1])
            valueList[value[0]] = vals
        else:
            valueList[value[0]].append(value[1])

    return valueList

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


def recommend(profparams):
    #print profparams['categories'].split(",")
    gp = GameProfile(int(profparams['min_players']), int(profparams['max_players']), int(profparams['player_age']), profparams['categories'].split(","), \
                    profparams['mechanics'].split(","), int(profparams['min_playing_time']), int(profparams['max_playing_time']))
    
    gp.displayGameProfile()

    games = generateCandidateGames()

    recommendations = obtainRecommendations(gp, games)

    recommendations.sort(key=lambda x: x.rating, reverse=True)

    return recommendations[:10]

if __name__ == '__main__':
    app.run(debug=True)
