import typing as t

from flask import Blueprint, request, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from landfile.models import User, Account

account = Blueprint('account', 'account', url_prefix='/account')


def get_acc() -> t.Tuple[User, Account]:

    username = get_jwt_identity()

    u: User = User.query.filter_by(username=username).first()

    if u is None:
        abort(500)

    assert isinstance(u, User)

    a: Account = Account.query.filter_by(crew_id=id).first_or_404()

    assert isinstance(a, Account)

    return u, a


@account.route('', methods=['GET'])
def get_account():

    user, acc = get_acc()

    return acc


@account.route('/billing', methods=['POST'])
@jwt_required
def post_billing(id: str):

    user, acc = get_acc()

    return acc


@account.route('/members', methods=['GET'])
@jwt_required
def post_billing(id: str):

    user, acc = get_acc()

    return acc.members


@account.route('/members', methods=['POST'])
@jwt_required
def post_billing(id: str):

    _, acc = get_acc()

    return acc.members


@account.route('/plan', methods=['POST'])
@jwt_required
def post_billing(id: str):

    _, acc = get_acc()

    return acc.plan
