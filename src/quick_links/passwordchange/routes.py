from flask import Blueprint, request, jsonify
from datetime import datetime
from .module import validate_password, change_user_password, logger

passwordchange_bp = Blueprint('passwordchange', __name__)

@passwordchange_bp.route('/change-password', methods=['POST'])
def change_password():
    logger.info("Password change request received")
    
    try:
        data = request.get_json()
        logger.debug(f"Received data: {data}")

        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        employee_code = data.get('employeeCode')

        if not all([old_password, new_password, employee_code]):
          logger.error("Missing required fields")
          return jsonify({'error': 'All fields are required'}), 400

        if not validate_password(new_password):
            logger.error("New password validation failed")
            return jsonify({'error': 'Invalid new password'}), 400

        success, message = change_user_password(employee_code, old_password, new_password)

        if success:
            return jsonify({
                'message': message,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({'error': message}), 400

    except Exception as e:
        logger.error(f"Server error: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500
