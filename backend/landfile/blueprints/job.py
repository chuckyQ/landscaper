import typing as t

from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User, Job

job = Blueprint('job', 'job', url_prefix='/jobs/<string:id>')


def get_job(id: str) -> t.Tuple[User, Job]:

    username = get_jwt_identity()

    u: User = User.query.filter_by(username=username).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    if not u.is_account_admin():
        abort(403)

    j: Job = Job.query.filter_by(job_id=id).first_or_404()

    assert isinstance(j, Job)

    return u, j


@job.route('', methods=['GET'])
@jwt_required
def get_job(id: str):
    user, job_ = get_job(id)
    return


@job.route('', methods=['POST'])
@jwt_required
def create_crew():
    ...

    # u = get_user()
