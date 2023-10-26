from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User

crews = Blueprint('crews', 'crews', url_prefix='/crews')


def get_user():

    username = get_jwt_identity()

    u: User = User.query.filter_by(username=username).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    return u


@crews.route('', methods=['GET'])
@jwt_required
def get_crews():

    u = get_user()
    return [u.crews + u.crew_leads]


@crews.route('', methods=['POST'])
@jwt_required
def create_crew():

    u = get_user()

    js = request.json

    crew = u.account.add_crew(name=js['name'])
    crew.members.append(u)
    crew.leads.append(u)

    crew.save()
