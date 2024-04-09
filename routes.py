from app import app, db
from flask import jsonify, request
from models import Review, User
from flask_jwt_extended import jwt_required


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


@app.route('/get_user_list', methods=['GET'])
@jwt_required()
def get_user_list():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    user_list.append(user_data)
    return jsonify(user_list)
