from app import app, db
from flask import jsonify, request
from models import Review, User
from flask_jwt_extended import jwt_required, get_jwt_identity


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


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.is_admin:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'success'}
    return {'message': 'you have not permissions'}


@app.route('/update_user_info/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_info(user_id):
    current_user = User.query.get(get_jwt_identity())
    user = User.query.get(user_id)
    if current_user == user or current_user.is_admin:
        data = request.json
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        db.session.commit()
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        return jsonify(user_info)
    else:
        return {'message': 'You have not permission'}, 403


# _______________________________________________________________________________________________________


@app.route('/create_review', methods=['POST'])
@jwt_required()
def create_review():
    current_user = User.query.get(get_jwt_identity())
    review_data = request.json
    review = Review(title=review_data['title'], desc=review_data['desc'], user=current_user)
    db.session.add(review)
    db.session.commit()
    return {'message': 'Review created successfully'}


@app.route('/review_list', methods=['GET'])
@jwt_required()
def review_list():
    reviews = Review.query.all()
    rev_list = []
    for review in reviews:
        review_data = {
            'id': review.id,
            'title': review.title,
        }
        rev_list.append(review_data)
    return jsonify(rev_list)


@app.route('/review_detail/<int:review_id>', methods=['GET'])
@jwt_required()
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {'message': 'Review not found'}, 404

    review_data = {
        'id': review.id,
        'title': review.title,
        'desc': review.desc,
        'created_at': review.created_at,
        'user_id': review.user_id
    }
    return jsonify(review_data)


@app.route('/update_review/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    current_user = User.query.get(get_jwt_identity())
    review = Review.query.get(review_id)
    if not review:
        return {'message': 'Review not found'}, 404

    if current_user == review.user or current_user.is_admin:
        data = request.json
        if 'title' in data:
            review.title = data['title']
        if 'desc' in data:
            review.desc = data['desc']
        db.session.commit()
        updated_review = {
            'id': review.id,
            'title': review.title,
            'desc': review.desc,
            'created_at': review.created_at,
            'user_id': review.user_id
        }
        return jsonify(updated_review)
    else:
        return {'message': 'You have not permission'}, 403


@app.route('/delete_review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    current_user = User.query.get(get_jwt_identity())
    review = Review.query.get(review_id)
    if not review:
        return {'message': 'Review not found'}, 404

    if current_user == review.user or current_user.is_admin:
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted successfully'}
    else:
        return {'message': 'You have not permission'}, 403
