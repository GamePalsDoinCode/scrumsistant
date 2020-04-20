from flask import Flask, request
from flask_cors import CORS
from flask_redis import FlaskRedis

try:
    from .local_settings import SERVER_NAME, REDIS_URL, REDIS_PASSWORD, REDIS_PORT
except:
    SERVER_NAME = 'me'
    REDIS_URL = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 0

REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/{REDIS_DB}'

app = Flask(__name__)
CORS(app)
redis_client = FlaskRedis(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/connect_user', methods=['POST'])
def connect_user():
	import pdb
	pdb.set_trace()
