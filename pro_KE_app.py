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
def query_games():
    # get data
    dict_input = request.get_json(force=True)

    print dict_input

    boardgamerecommender.main(dict_input)

    result = {'success': 'true', 'message': 'Heuy fissa', 'data': 'dummy dummy'}
    return json.dumps(result)


@app.route('/get_form_options/', methods=['POST'])
def get_form_options():
    # dummy queries
    categories_list = ['one', 'two', 'three']
    mechanics_list = ['four', 'five', 'six']
    checkboxes = {'categories': categories_list, 'mechanics': mechanics_list}

    result = {'success': 'true', 'message': 'Here are the dropdowns', 'data': checkboxes}
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
