from datetime import datetime

from flask import Flask, jsonify, abort, request
from flask_bcrypt import Bcrypt

from db.db_operations import *
from validation import check_user, check_advertisement

app = Flask(__name__)
bc = Bcrypt(app)


@app.route('/api/v1/hello-world/17')
def index():
    return "Hello World 17"


@app.route('/api/v1/advertisements', methods=['GET'])
def get_advertisements():
    code, response = get_all_advertisements()
    if code != 200:
        abort(code)
    return jsonify(response)


@app.route('/api/v1/advertisement/byRegion/<int:id>', methods=['GET'])
def get_advertisements_by_region_id(id):
    if id not in get_all_id(Region):
        abort(404)
    code, response = get_all_advertisements_by_region(id)
    if code != 200:
        abort(code)
    return jsonify(response)


@app.route('/api/v1/auth/register', methods=['POST'])
def register_new_user():
    if not request.json:
        abort(400)
    if not check_user(User, request):
        abort(400)

    user = {col: request.json.get(col, None) for col in User.__table__.columns.keys()[1:]}
    user["password"] = bc.generate_password_hash(user["password"], rounds=4).decode('UTF-8')
    if user.get("username", "") in get_all_usernames():
        abort(400)
    response = create_user(**user)
    del user["password"]
    if isinstance(response, tuple):
        return response[1], response[0]
    return jsonify(user), response


@app.route('/api/v1/advertisement/<int:id>', methods=['PUT'])
def change_advertisement(id):
    if not request.json:
        abort(400)
    if id not in get_all_id(Advertisement):
        abort(404)
    if not check_advertisement(Advertisement, request):
        abort(400)

    response = update_advertisement(id, **request.json)
    print(response)
    if str(response[0])[0] != '2':
        abort(400)
    return jsonify(response[1]), response[0]


@app.route('/api/v1/advertisement', methods=['POST'])
def add_new_advertisement():
    if not request.json:
        abort(400)
    if not check_advertisement(Advertisement, request):
        abort(400)

    advertisement = {col: request.json.get(col, None) for col in Advertisement.__table__.columns.keys()[1:]}
    advertisement["date_of_publishing"] = datetime.now()
    response = create_advertisement(**advertisement)
    if isinstance(response, tuple):
        return response[1], response[0]
    return jsonify(advertisement), response


@app.route('/api/v1/advertisement/<int:id>', methods=['DELETE'])
def delete_advertisement(id):
    if not isinstance(id, int):
        abort(400)
    if id not in get_all_id(Advertisement):
        abort(404)
    response = delete_advertisement_by_id(id)
    if isinstance(response, tuple):
        return response[1], response[0]
    return response


@app.route('/api/v1/user/<string:user_name>', methods=['GET'])
def get_user(user_name):
    if user_name not in get_all_usernames():
        abort(404)
    code, response = get_user_by_username(user_name)
    if code != 200:
        print(response)
        abort(code)
    del response["password"], response["id"]
    response["region"] = get_region(response["region_id"])
    del response["region_id"]
    return jsonify(response)


@app.route('/api/v1/user/<user_name>', methods=['PUT'])
def change_user(user_name):
    if user_name not in get_all_usernames():
        abort(404)
    if not request.json or not check_user(User, request):
        abort(400)
    updated_columns = request.json
    response = update_user(user_name, **updated_columns)
    return jsonify(response[1]), response[0]


if __name__ == "__main__":
    app.run(debug=True)
