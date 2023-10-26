from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User

tasks = Blueprint('tasks', 'tasks', url_prefix='/tasks')


def get_user():

    username = get_jwt_identity()

    u: User = User.query.filter_by(username=username).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    if not u.is_account_admin():
        abort(403)

    return u


@tasks.route('', methods=['GET'])
@jwt_required
def get_tasks():
    u = get_user()
    return [u.tasks]


@tasks.route('', methods=['POST'])
@jwt_required
def create_crew():

    u = get_user()
