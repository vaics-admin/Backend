# src/employee_profile/__init__.py
from flask import Blueprint

# Initialize the employee_profile blueprint
employee_profile_bp = Blueprint('employee_profile', __name__)

# from . import routes