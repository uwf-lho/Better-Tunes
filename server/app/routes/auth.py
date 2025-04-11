from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import create_access_token

from app.utils.tools import validate_json

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login. Verifies user credentials and returns an access token if valid.

    Returns:
        JSON: Access token and token type if credentials are valid, otherwise an error message.
    """
    data, error_response, status_code = validate_json(['username', 'password'])
    if error_response:
        return error_response, status_code

    username, password = data['username'], data['password']
    user_service = current_app.user_service
    user = user_service.get_user_by_username(username)

    # Verify user password and generate access token if valid
    if user and user_service.verify_password(password, user['password']):
        access_token = create_access_token(identity=username)
        return jsonify({
            'access_token': access_token,
            'token_type': 'bearer',
        }), 200

    return jsonify({'msg': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint for user registration. Registers a new user and returns an access token if successful.

    Returns:
        JSON: Access token and message if registration is successful, otherwise an error message.
    """
    data, error_response, status_code = validate_json(['username', 'password'])
    if error_response:
        return error_response, status_code

    username, password = data['username'], data['password']
    user_service = current_app.user_service

    # Attempt to register the user
    message, status_code = user_service.register_user(username, password)
    message = message.get('msg')

    if status_code == 201:
        access_token = create_access_token(identity=username)
        return jsonify({
            'access_token': access_token,
            'token_type': 'bearer',
            'msg': message,
        }), 201

    return jsonify({'msg': message}), 400
