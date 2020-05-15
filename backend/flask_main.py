import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_redis import FlaskRedis

from .flask_utils import load_user, login_required_by_default
from .local_settings import FLASK_SECRET_KEY, REDIS_CONNECTION_URL
from .scrum_types import RedisClient
from .structs import AnonymousUserWrapper


def public_endpoint(function):
    function.is_public = True
    return function


def create_app(test_config=None):
    # pylint: disable=import-outside-toplevel
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    app.secret_key = FLASK_SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # login session lifetime.  can be any timedelta obj

    if test_config:
        redis_client: RedisClient = test_config['redis']
        app.config.update(test_config)
    else:
        app.config['REDIS_URL'] = REDIS_CONNECTION_URL
        redis_client: RedisClient = FlaskRedis(app)

    app.redis_client: RedisClient = redis_client
    login_service = LoginManager(app)
    app.login_service = login_service
    login_service.anonymous_user = AnonymousUserWrapper
    login_service.user_loader(load_user)
    CORS(app)

    from .flask_auth import bp as auth_bp
    from .flask_current_users_api import bp as cur_users_api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cur_users_api_bp)
    app.before_request(login_required_by_default)
    return app


if not os.environ.get('TRAVIS'):  # true when run in CI # pragma: no cover
    app = create_app()
