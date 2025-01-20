import bcrypt
import logging
from datetime import datetime
from src.app import db
from src.module import VaicsData

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def validate_password(password):
    """
    Validate the password meets security requirements.
    Add your password validation logic here.
    """
    if not password or len(password) < 8:
        return False
    return True

def is_bcrypt_hash(password):
    """Check if the password is already a bcrypt hash."""
    try:
        return password.startswith('$2b$') or password.startswith('$2a$')
    except:
        return False

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def change_user_password(employee_code, old_password, new_password):
    """
    Change user password with validation.
    """
    try:
        employee = VaicsData.query.filter_by(empcode=employee_code).first()
        if not employee:
            logger.error(f"Employee not found: {employee_code}")
            return False, "Employee not found"

        stored_password = employee.password
        password_verified = False

        if stored_password:
            if is_bcrypt_hash(stored_password):
                try:
                    password_verified = bcrypt.checkpw(
                        old_password.encode('utf-8'),
                        stored_password.encode('utf-8')
                    )
                except Exception as e:
                    logger.error(f"Error verifying hashed password: {e}")
                    password_verified = False
            else:
                password_verified = (old_password == stored_password)

        if not password_verified:
            return False, "Current password is incorrect"

        hashed_new_password = hash_password(new_password)
        employee.password = hashed_new_password
        db.session.commit()

        return True, "Password changed successfully"

    except Exception as e:
        logger.error(f"Error changing password: {e}")
        db.session.rollback()
        return False, f"Server error: {str(e)}"
