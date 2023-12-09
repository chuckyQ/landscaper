from flask import Blueprint, abort

from flask_jwt_extended import jwt_required

from landfile.models import User
from landfile.schema import schema
from landfile.schema.api import validate

crews = Blueprint('crews', 'crews', url_prefix='/crews')


def get_user():

    u: User = User.query.all()[0]

    if u is None:
        abort(500)

    assert isinstance(u, User)

    return u


@crews.route('', methods=['GET'])
# @jwt_required
def get_crews():

    u = get_user()
    return [c.json() for c in u.account.crews]


@crews.route('', methods=['POST'])
@validate(
  name=schema.String(),
  description=schema.String(),
  color=schema.String(),
  useBlackText=schema.Boolean(),
  members=schema.Array(schema.String, minsize=0)
)
def create_crew(name: str, description: str, color: str, useBlackText: str, members: list):

    u = get_user()
    account = u.account
    crew = account.add_crew(name=name, description=description,
                            color=color, use_black_text=useBlackText)

    users_ = []
    for email in members:

        u = account.get_user(email)
        if u is None:
            abort(500)
        users_.append(u)

    crew.members.clear()
    crew.members.extend(users_)
    crew.save()
    return {}
