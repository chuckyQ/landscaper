from flask import Flask
from flask_cors import CORS
from events import socketio

from flask import Blueprint

main = Blueprint('main', 'main')

@main.route('/')
def connect_to_main():
    ...


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(main)

    socketio.init_app(app, cors_allowed_origins="*")
    return app

if __name__ == '__main__':
    app = create_app(debug=True)
    socketio.run(app, port=5001)
