# all the imports
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import boardgamerecommender

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    return app.send_static_file('client.html')


@app.route('/query_games/', methods=['POST'])
def sign_in():
    # get data
    dict_input = request.get_json(force=True)

    boardgamerecommender.main(dict_input)

    print dict_input
    result = {'success': 'true', 'message': 'Heuy fissa', 'data': 'dummy dummy'}
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
