from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import FlaskRedis

from .local_settings import FLASK_SECRET_KEY, REDIS_CONNECTION_URL
from .scrum_types import RedisClient
from .structs import AnonymousUserWrapper


def public_endpoint(function):
    function.is_public = True
    return function


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # login session lifetime.  can be any timedelta obj
    app.config['REDIS_URL'] = REDIS_CONNECTION_URL
    redis_client: RedisClient = FlaskRedis(app)
    app.redis_client = redis_client
    # redis_pub_sub = redis_client.pubsub(ignore_subscribe_messages=True,)
    login_service = LoginManager(app)
    app.login_service = login_service
    login_service.anonymous_user = AnonymousUserWrapper
    CORS(app)
    return app


app = create_app()

# these need to be below the app init to avoid circular imports
# pylint: disable=unused-import
from . import flask_auth  # isort:skip
from . import flask_current_users_api  # isort:skip
