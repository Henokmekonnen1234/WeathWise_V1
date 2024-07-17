

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from models import storage
from uuid import uuid4

app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["SECRET_KEY"] = str(uuid4())
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*/": {"origins": "*"}})
jwt = JWTManager(app)


@app.before_request
def open_mongodb():
    storage.reload()


@app.teardown_appcontext
def close_mongodb(error):
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': f"{error}"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)