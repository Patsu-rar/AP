from datetime import datetime

from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth

from db.db_operations import *
from db.models import Session
from validation import check_user, check_advertisement
from passlib.hash import bcrypt

app = Flask(__name__)
bc = Bcrypt(app)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    u = Session.query(User).filter_by(username=username).first()
    if not u or not bcrypt.verify(password, u.password):
        return False
    return True


@app.route('/api/v1/hello-world/17')
def index():
    return "Hello World 17"


@app.route('/api/v1/advertisements', methods=['GET'])
def get_advertisements():
    code, response = get_all_advertisements()
    if code != 200:
        return {"message": str(response)}, code
    return jsonify(response)


@app.route('/api/v1/advertisement/byRegion/<int:id>', methods=['GET'])
@auth.login_required()
def get_advertisements_by_region_id(id):
    if id not in get_all_id(Region):
        return {"message": "Region can not be found"}, 404
    code, response = get_all_advertisements_by_region(id)
    if code != 200:
        return {"message": str(response)}, code

    u = Session.query(User).filter_by(username=auth.current_user()).first()
    if u.region_id != id:
        return {"message": "Forbidden operation"}, 403

    return jsonify(response)


@app.route('/api/v1/auth/register', methods=['POST'])
def register_new_user():
    if not request.json:
        return {"message": "Incorrect body"}, 400
    if not check_user(User, request):
        return {"message": "Incorrect body"}, 400

    user = {col: request.json.get(col, None) for col in User.__table__.columns.keys()[1:]}
    user["password"] = bc.generate_password_hash(user["password"], rounds=4).decode('UTF-8')
    if user.get("username", "") in get_all_usernames():
        return {"message": "Incorrect body"}, 400
    response = create_user(**user)
    del user["password"]
    if isinstance(response, tuple):
        return response[1], response[0]
    return jsonify(user), 200


@app.route('/api/v1/advertisement/<int:add_id>', methods=['PUT'])
@auth.login_required()
def change_advertisement(add_id):
    if not request.json:
        return {"message": "Incorrect body"}, 400
    if add_id not in get_all_id(Advertisement):
        return {"message": "Missing advertisement"}, 404
    if not check_advertisement(Advertisement, request):
        return {"message": "Incorrect body"}, 400

    u = Session.query(User).filter_by(username=auth.current_user()).first()
    adds = Session.query(Advertisement.user_id).filter_by(id=add_id).first()
    if u.id != adds[0]:
        return {"message": "Forbidden operation"}, 403

    code, response = update_advertisement(add_id, **request.json)
    if code == 200:
        return {"message": str(response)}, code
    return jsonify(response[1]), response[0]


@app.route('/api/v1/advertisement', methods=['POST'])
@auth.login_required()
def add_new_advertisement():
    if not request.json:
        return {"message": "Incorrect body"}, 400
    if not check_advertisement(Advertisement, request):
        return {"message": "Incorrect body"}, 400

    u = Session.query(User).filter_by(username=auth.current_user()).first()
    if u.id != request.json["user_id"]:
        return {"message": "Forbidden operation"}, 403

    advertisement = {col: request.json.get(col, None) for col in Advertisement.__table__.columns.keys()[1:]}
    advertisement["date_of_publishing"] = datetime.now()
    response = create_advertisement(**advertisement)
    if isinstance(response, tuple):
        return response[1], response[0]
    return jsonify(advertisement), 200


@app.route('/api/v1/advertisement/<int:add_id>', methods=['DELETE'])
@auth.login_required()
def delete_advertisement(add_id):
    if add_id not in get_all_id(Advertisement):
        return {"message": "Advertisement can not be found"}, 404

    u = Session.query(User).filter_by(username=auth.current_user()).first()
    adds = Session.query(Advertisement.user_id).filter_by(id=add_id).first()
    if u.id != adds[0]:
        return {"message": "Forbidden operation"}, 403

    response = delete_advertisement_by_id(add_id)
    if isinstance(response, tuple):
        return response[1], response[0]
    return response


@app.route('/api/v1/user/<string:user_name>', methods=['GET'])
def get_user(user_name):
    if user_name not in get_all_usernames():
        return {"message": "User can not be found"}, 404
    code, response = get_user_by_username(user_name)
    if code != 200:
        return {"message": str(response)}, code
    del response["password"], response["id"]
    response["region"] = get_region(response["region_id"])
    del response["region_id"]
    return jsonify(response)


@app.route('/api/v1/user/advertisements/<int:id>', methods=['GET'])
@auth.login_required()
def get_user_advertisements(id):
    if id not in get_all_id(User):
        return {"message": "User can not be found"}, 404

    u = Session.query(User).filter_by(username=auth.current_user()).first()
    if u.id != id:
        return {"message": "Forbidden operation"}, 403

    code, response = get_all_ads_for_user(id)
    if code != 200:
        return {"message": str(response)}, code
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
