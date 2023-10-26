import os
import re

from dotenv import load_dotenv

load_dotenv()

from flask import Blueprint, abort, jsonify, request, make_response, render_template, current_app

from flask_jwt_extended import create_access_token
from sqlalchemy import func

from landfile.models import User
from planfile import payment
from planfile.emailer import send_support_email
from planfile.security import generate_password

from planfile.schema.api import validate, schema

public = Blueprint('public', __name__, url_prefix='/')


@public.route('/register', methods=['POST'])
@validate(
    username = schema.String(minsize=1,
                             maxsize=38,
                             regex=re.compile(r'^[a-z\\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$', re.IGNORECASE),
                             ),
    email = schema.String(),
)
def register():

    from planfile.models import create_free_account

    j = request.json

    username: str = j['username'].strip()
    email: str = j['email'].strip()

    u = User.query.filter(func.lower(User.username) == username.lower()).first()
    if u is not None:
        return {'msg' : 'This username is already in use.'}, 401

    u = User.query.filter(func.lower(User.email) == email.lower()).first()
    if u is not None:
        return {'msg' : 'This email is already in use.'}, 401

    cust_id = payment.create_account(username, email)

    acc = create_free_account(username, cust_id, testing=current_app.config['TESTING'])

    password = generate_password()

    user = acc.create_user(username, password, email)

    t = acc.create_team('Personal Projects', 'My personal projects')
    t.admins.append(user)
    t.members.append(user)

    send_support_email('Your new PlanFile account is ready!', email,
                        message=render_template('new_user.html',
                                                username=username,
                                                password=password)
    )

    acc.save()
    t.save()
    user.save()

    return make_response(jsonify({'msg': 'Success'}), 200)


@public.route('/login', methods=['POST'])
@validate(
    username = schema.String(),
    password = schema.String(),
)
def login():
    """
    When a user logs in, they will be provided with a
    JWT used for accessing other endpoints.

    The required json is

        {
            'username' : username,
            'password', password
        }
    """

    from planfile.models import User

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username is None or password is None:
        abort(401)

    u: User = User.get(username.lower())

    if u is None:
        abort(401)

    if not u.verify_password(password):
        abort(401)

    access_token = create_access_token(identity=u.username)
    response = jsonify(msg='login successful', access_token=access_token,
                       isAccountOwner=u.is_account_owner())
    return response


@public.route('/inquiry', methods=['POST'])
@validate(
    name=schema.String(),
    phone=schema.String(),
    company=schema.String(),
    email=schema.String(),
    country=schema.String(),
    how=schema.String(),
    moreInfo=schema.String(),
)
def inquiry():

    import html

    from planfile.emailer import send_support_email

    data = {key : html.escape(val) for key, val in request.json.items()}

    tmpl = render_template('inquiry.html', **data)

    try:
        send_support_email(subject='PlanFile Inquiry', to='support@planfile.com', message=tmpl)
    except:
        abort(500)

    return {}
