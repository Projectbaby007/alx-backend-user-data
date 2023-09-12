#!/usr/bin/env python3

""" Handles all routes for the Session authentication
"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Creates a new session after retrieving the user
    from email and password
    """
    from api.v1.app import auth
    from models.user import User

    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Deletes the current session
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200