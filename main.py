from flask import Flask
from flask import request
import json

app = Flask(__name__)

# read files
with open('./data/user.json') as json_file:
    user_data = json.load(json_file)

with open('./data/lists.json') as json_file:
    list_data = json.load(json_file)

@app.route('/list', methods=['POST'])
def get_lists():
    data = json.load(json_file)
    return data

@app.route('/list/<list_id>', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return xxx
    else:
        return xxx