from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User

jobs = Blueprint('jobs', 'jobs', url_prefix='/jobs')


def get_user():

    email = get_jwt_identity()

    u: User = User.query.filter_by(email=email).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    if not u.is_account_admin():
        abort(403)

    return u


@jobs.route('', methods=['GET'])
@jwt_required
def get_jobs():
    u = get_user()
    return [u.jobs]


@jobs.route('', methods=['POST'])
@jwt_required
def create_crew():

    u = get_user()
