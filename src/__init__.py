import os
import logging

from flask import Flask, redirect,  url_for
from flask.cli import load_dotenv


def create_app(test_config=None):
    # shell env -> .env -> .flaskenv -> os.environ
    load_dotenv()

    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=os.environ['SECRET_KEY'],
        # store the database in the instance folder
        DATABASE=os.environ['DATABASE'],
        SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI']
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', endpoint='index')
    def hello():
        return redirect(url_for("speech.list"))

    # register the database commands (sqlite3)
    # from . import db
    # db.init_app(app)

    # register the database commands (sqlalchemy)
    from . import db
    db.init_app(app)

    with app.app_context():
        db.init_db()

    # apply the blueprints to the app
    from .views.user import bp as user_bp
    from .views.speech import bp as speech_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(speech_bp)

    # dynamically create url rules for the index view
    app.add_url_rule('/', endpoint='index')

    return app
