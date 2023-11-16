from flask import Blueprint, abort, request

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User

user = Blueprint('user', 'user', url_prefix='/users/<string:id>')


def get_user(id: str) -> User:

    return User.query.filter_by(user_id=id).first_or_404()


@user.route('', methods=['GET'])
# @jwt_required
def _get_user(id: str):
    u = get_user(id)
    return u.json()


@user.route('', methods=['POST'])
# @jwt_required
def update_user(id: str):

    u = get_user(id)

    for key, val in request.json.items():
        setattr(u, key, val)

    u.phone_number = request.json['phoneNumber']
    u.save()
    return {}

