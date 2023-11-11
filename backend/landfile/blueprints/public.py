from flask import Blueprint, abort, jsonify, request, make_response, render_template

from flask_jwt_extended import create_access_token
from sqlalchemy import func

from landfile.models import User
from landfile.security import generate_password
public = Blueprint('public', __name__, url_prefix='/')


@public.route('/register', methods=['POST'])
def register():

    from landfile.models import create_account

    j = request.json

    email: str = j['email'].strip()

    u = User.query.filter(func.lower(User.email) == email.lower()).first()
    if u is not None:
        return {'msg' : 'This email is already in use.'}, 401

    password = generate_password()
    acc = create_account(email, password)
    user = acc.add_user(email, password)

    send_support_email('Your new PlanFile account is ready!', email,
                        message=render_template('new_user.html', password=password))

    acc.save()
    user.save()

    return make_response(jsonify({'msg': 'Success'}), 200)


@public.route('/login', methods=['POST'])
def login():


    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None or password is None:
        abort(401)

    u: User = User.get(email.lower())

    if u is None:
        abort(401)

    assert isinstance(u, User)

    if not u.verify_password(password):
        abort(401)

    access_token = create_access_token(identity=u.email)
    response = jsonify(msg='login successful', access_token=access_token,
                       isAccountOwner=u.is_account_owner())
    return response
