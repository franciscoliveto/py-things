from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_claims, get_jwt_identity, get_raw_jwt
)


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'
# Enable blacklisting and specify what kind
# of tokens to check against the blacklist
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

# A storage engine to save revoked tokens.
blacklist = set()


def generate_hash(password):
    return password


def verify_hash(password, hash):
    return password == hash


users = [{'username': 'franciscoliveto', 'password': generate_hash('123456')},
         {'username': 'juan', 'password': generate_hash('6543421')}]


def get_users(username):
    return next((u for u in users if u.get('username') == username), None)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify(msg='Missing JSON in request'), 400

    json_data = request.json
    username = json_data.get('username', None)
    password = json_data.get('password', None)
    if not username:
        return jsonify(msg='Missing username parameter'), 400
    if not password:
        return jsonify(msg='Missing password parameter'), 400

    current_user = get_users(username)
    if not current_user:
        return jsonify(msg='Bad username or password'), 401

    if not verify_hash(password, current_user.get('password')):
        return jsonify(msg='Bad username or password'), 401

    access_token = create_access_token(identity=username, user_claims={'role': 'admin'})
    return jsonify(access_token=access_token), 200

# This decorator sets the callback function that will be called when a protected endpoint is
# accessed and will check if the JWT has been revoked. By default, this callback is not used.
# The callback must be a function that takes one argument, which is the decoded JWT (python dictionary),
# and returns `True` if the token has been blacklisted (or is otherwise considered revoked), or `False` otherwise.
@jwt.token_in_blacklist_loader
def is_token_in_blacklist(decoded_token):
    # We are just checking if the tokens jti
    # (unique identifier) is in the blacklist set.
    jti = decoded_token['jti']
    return jti in blacklist


@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    # get_raw_jwt(): In a protected endpoint, this will return the python dictionary
    # which has all of the claims of the JWT that is accessing the endpoint.
    # If no JWT is currently present, an empty dict is returned instead.
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify(msg='Successfully logged out'), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    claims = get_jwt_claims()
    return jsonify(logged_in_as=current_user, user_claims=claims), 200
