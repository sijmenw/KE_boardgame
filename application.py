import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from gameprofile import GameProfile
from game import Game
import MySQLdb
import credentials
from operator import itemgetter

##################################################################################
#                                                                                #
#                           WEB APPLICATION CODE                                 #
#                                                                                #
##################################################################################

# Create the web application
app = Flask(__name__)
app.config.from_object(__name__)

# Get the .html file to display the form
@app.route('/')
def home():
    return app.send_static_file('client.html')

# Send form data to the recommender application and obtain the result
@app.route('/query_games/', methods=['POST'])
def query_games():
    # get data
    dict_input = request.get_json(force=True)

    recommendations = rankedRecommendation(dict_input)
    resultData = []
    
    for r in recommendations:
        resultData.append(r.__dict__)

    result = {'success': 'true', 'message': 'Heuy fissa', 'data': resultData}
    return json.dumps(result)

# Helper function: get all possible values from categories and mechanics from the databse
@app.route('/get_form_options/', methods=['POST'])
def get_form_options():
    categoriesQuery = "select distinct category from boardgame_category;"
    mechanicsQuery = "select distinct mechanics from boardgame_mechanics;"

    categories_list = getDistinctOptions(categoriesQuery)
    mechanics_list = getDistinctOptions(mechanicsQuery)

    checkboxes = {'categories': categories_list, 'mechanics': mechanics_list}

    result = {'success': 'true', 'message': 'Here are the dropdowns', 'data': checkboxes}
    return json.dumps(result)

# Helper function: query the database, get resultset and return it as a list
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

##################################################################################
#                                                                                #
#                         BOARD GAME RECOMMENDER CODE                            #
#                                                                                #
##################################################################################

#TASK createGameProfile:
# ROLES:
#   INPUT: user form input;
#   OUTPUT: GameProfile object;
#END TASK createGameProfile;

#WHILE NEW-PROFILE create(candidate-classes -> attribute)
#     obtain(attribute -> new-feature);
#     current-feature-set := new-feature ADD current-feature-set;
def createGameProfile(formParams):
    return GameProfile(int(formParams['min_players']), int(formParams['max_players']), int(formParams['player_age']), formParams['categories'].split(","), \
                    formParams['mechanics'].split(","), int(formParams['min_playing_time']), int(formParams['max_playing_time']))

#TASK obtainRecommendations;
# ROLES:
#   INPUT: object: "Game profile";
#   OUTPUT: candidate-classes: "Set of games matching input";
#END TASK obtainRecommendations;

def obtainRecommendations(gameProfile):
    games = generateCandidateGames()

    recommendations = match(gameProfile, games)

    return recommendations

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

        games = []

        for gameRes in gameResults:
            game = specifyAndObtainAttributes(gameRes, categoriesDict, mechanicsDict)
            games.append(game)

    except Exception as e:
        print "Error: unable to fetch data" + str(e)

    db.close()
    return games

# Helper function for generateCandidateGames
# Get list of attribute values for attributes that allow multiple values
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

def specifyAndObtainAttributes(game, categoriesDict, mechanicsDict):
    description = ""
    categories = []
    mechanics = []

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
                        mechanics, description, playing_time, expansion, "test", [], \
                        [], rating)

    return game

#     FOR-EACH class IN candidate-classes DO
#       match(class + current-feature-set -> truth-value);
#     IF truth-value == false
#     THEN
#       candidate-classes := candidate-classes SUBTRACT class;
#     END IF
#   END FOR-EACH
def match(gameProfile, games):
    recommendations = []

    for game in games:
        if matchFeatureSet(gameProfile, game):
            recommendations.append(game)

    return recommendations

# Knowledge base specified by rule types
# Match inference step
def matchFeatureSet(gameProfile, game):

    return (game.min_players >= gameProfile.min_players and 
            game.max_players <= gameProfile.max_players and
            game.player_age >= gameProfile.player_age and 
            game.playing_time >= gameProfile.min_playing_time and 
            game.playing_time <= gameProfile.max_playing_time and 
            matchList(game.categories, gameProfile.categories) and 
            matchList(game.mechanics, gameProfile.mechanics))

# Helper function for matchFeature set
# Use this to match attributes with multiple values (categories and mechanics)
# The function checks if there is an overlap between features that allow multiple values (set intersection)
def matchList(gameProfileFeatures, gameFeatures):
    return len(list(set(gameProfileFeatures) & set(gameFeatures))) > 0

# Get the top 10 recommendations based on user rating
def rankedRecommendation(formParams):
    gp = createGameProfile(formParams)

    recommendations = obtainRecommendations(gp)

    # rank(candidate-classes)
    recommendations.sort(key=lambda x: x.rating, reverse=True)

    return recommendations[:10]

if __name__ == '__main__':
    app.run(debug=True)
