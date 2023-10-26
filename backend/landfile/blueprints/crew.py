import typing as t

from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User, Crew

crew = Blueprint('crew', 'crew', url_prefix='/crews/<string:id>')


def get_crew(id: str) -> t.Tuple[User, Crew]:

    username = get_jwt_identity()

    u: User = User.query.filter_by(username=username).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    c: Crew = Crew.query.filter_by(crew_id=id).first_or_404()

    assert isinstance(c, Crew)

    if u not in c.members:
        abort(403)

    return u, c


@crew.route('', methods=['POST'])
@jwt_required
def post_crew(id: str):

    user, crew_ = get_crew(id)

    if user not in crew_.leads:
        abort(403)

    return crew
