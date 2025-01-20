from flask import Blueprint, request, jsonify
import bcrypt
from .module import get_user_by_empcode

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204  # Handle preflight CORS request

    try:
        data = request.json
        print(data)
        empcode = data.get("userName")
        password = data.get("password")

        if not empcode or not password:
            return jsonify({"message": "Username and password are required"}), 400

        # Fetch user from the database
        user = get_user_by_empcode(empcode)

        if user:
            stored_password = user.password

            if stored_password:
                if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):  # Check if bcrypt hash
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        return jsonify({"message": "Login successful"}), 200
                    else:
                        return jsonify({"message": "Invalid credentials"}), 401
                else:
                    # Handle plaintext password for backward compatibility
                    if password == stored_password:
                        return jsonify({"message": "Login successful"}), 200
                    else:
                        return jsonify({"message": "Invalid credentials"}), 401

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "Internal server error"}), 500
