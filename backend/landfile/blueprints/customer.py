from flask import Blueprint, request, abort, jsonify

from flask_jwt_extended import jwt_required

from landfile.models import User, Customer

customer = Blueprint('customer', 'customer', url_prefix='/customers/<string:id>')


def get_account():

    u: User = User.query.all()[0]

    return u.account


@customer.route('', methods=['GET'])
# @jwt_required
def get_customers(id: str):
    acc = get_account()
    c = Customer.query.filter_by(cust_id=id).first_or_404()
    return c.json()
