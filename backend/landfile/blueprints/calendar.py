import typing as t

from flask import Blueprint, request, abort, jsonify
from flask_jwt_extended import jwt_required
from landfile.models import User

calendar = Blueprint('calendar', 'calendar', url_prefix='/calendar')


def get_account():

    u: User = User.query.all()[0]

    return u.account


@calendar.route('', methods=['GET'])
# @jwt_required
def get_jobs():

    from landfile.models import Job

    acc = get_account()

    start_timestamp = request.args.get('startTimestamp')
    end_timestamp = request.args.get('endTimestamp')

    jobs: t.List[Job] = Job.query.filter(Job.account_id == u.account.id,
                            Job.work_date_timestamp >= start_timestamp,
                            Job.work_date_timestamp < end_timestamp).all()

    return jsonify([c.json() for c in jobs])
