import typing as t

from flask import Blueprint, request, abort, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User, Crew
from landfile.schema.api import validate
from landfile.schema import schema

crew = Blueprint('crew', 'crew', url_prefix='/crews/<string:id>')


def _get_crew(id: str) -> t.Tuple[User, Crew]:

    u: User = User.query.all()[0]

    if u is None:
        abort(500)

    assert isinstance(u, User)

    c: Crew = Crew.query.filter_by(crew_id=id).first_or_404()

    assert isinstance(c, Crew)

    # if u not in c.members:
    #     abort(403)

    return u, c


@crew.route('', methods=['GET'])
# @jwt_required
def get_crew(id: str):

    _, crew_ = _get_crew(id)

    return crew_.json(get_members=True)


@crew.route('', methods=['POST'])
# @jwt_required
# @jwt_required
@validate(
    name=schema.String(),
    description=schema.String(),
    members=schema.Array(schema.String, minsize=0),
    color=schema.String(),
    useBlackText=schema.Boolean(),
    crewID=schema.String(),
)
def post_crew(id: str, crewID: str, name: str, description: str, members: list, color: str, useBlackText: bool):

    _, crew_ = _get_crew(id)

    crew_.name = name
    crew_.description = description
    crew_.color = color
    crew_.use_black_text = useBlackText

    acc = user.account

    _members = []
    for member in members:
        user = acc.get_user(member)
        if user is None:
            abort(500)

        _members.append(user)

    crew_.members.clear()
    crew_.members.extend(_members)

    crew_.save()
    return {}


@crew.route('', methods=['DELETE'])
def delete_crew(id: str):

    _, crew_ = _get_crew(id)

    crew_.jobs.clear()
    crew_.members.clear()
    crew_.delete()

    return {}

@crew.route('/members', methods=['GET'])
# @jwt_required
def get_crew_members(id: str):

    user, crew_ = _get_crew(id)

    user_ids = {u.user_id for u in crew_.members}

    users = []
    for user in user.account.members:

        js = user.json()
        js['inCrew'] = user.user_id in user_ids
        users.append(js)

    return  jsonify(users)


@crew.route('/members', methods=['POST'])
# @jwt_required
def save_crew_members(id: str):

    user, crew_ = _get_crew(id)

    crew_.members.clear()
    each: dict
    for each in request.json:

        if each['inCrew']:

            u: User = User.query.filter_by(user_id=each['userID']).first()
            if u is None:
                # Should not happen
                continue
            assert isinstance(u, User)
            crew_.members.append(u)

    crew_.save()

    return {}
