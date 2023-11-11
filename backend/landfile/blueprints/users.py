from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User

users = Blueprint('users', 'users', url_prefix='/users')


def get_user():


    u: User = User.query.all()[0]

    if u is None:
        abort(500)

    assert isinstance(u, User)

    if not u.is_admin:
        abort(403)

    return u


@users.route('', methods=['GET'])
# @jwt_required
def get_users():
    u = get_user()
    return [u.json() for u in u.account.members]


@users.route('', methods=['POST'])
# @jwt_required
def create_user():


    js = request.json

    u = get_user()
    acc = u.account
    acc.add_user(email=js['email'], phone_number=js['phoneNumber'], password='abcdef', is_admin=False)
    return {}
