from flask import Blueprint, request, abort, jsonify

from flask_jwt_extended import jwt_required

from landfile.models import User

customers = Blueprint('customers', 'customers', url_prefix='/customers')


def get_account():

    u: User = User.query.all()[0]

    return u.account


@customers.route('', methods=['GET'])
# @jwt_required
def get_customers():
    acc = get_account()
    return jsonify([c.json() for c in acc.customers])


@customers.route('', methods=['POST'])
# @jwt_required
def add_customer():

    acc = get_account()

    js = request.json

    acc.add_customer(address=js['address'], contact_name=js['name'], phone_number=js['phoneNumber'], notes='')

    return {}
