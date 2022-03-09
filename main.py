import json
import uuid

from flask import Flask, request, jsonify, abort

app = Flask(__name__)


# add some headers to allow cross-origin access to the API
# on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# read files
with open('./data/users.json') as json_file:
    user_data = json.load(json_file)

with open('./data/lists.json') as json_file:
    list_data = json.load(json_file)

with open('./data/todos.json') as json_file:
    todo_data = json.load(json_file)


@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(list_data)


# define endpoint for adding a new list
@app.route('/list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = uuid.uuid4()
    list_data.append(new_list)
    return jsonify(new_list), 200


# define endpoint for getting and deleting existing todo lists
@app.route('/list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in list_data:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todo_data if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        list_data.remove(list_item)
        return '', 200

# define endpoint for getting and deleting existing todo lists
@app.route('/list/<list_id>/entry', methods=['POST'])
def add_new_list_entry(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in list_data:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # make JSON from POST data (even if content type is not set correctly)
    new_list_entry = request.get_json(force=True)
    print('Got new entry to be added: {}'.format(new_list_entry))
    # create id for new entry, save it and return the entry with id
    new_list_entry['id'] = uuid.uuid4()
    new_list_entry['list_id'] = list_item['id']
    # add entry to todos.json and safe with list_id
    todo_data.append(new_list_entry)
    return jsonify(new_list_entry), 200



if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
