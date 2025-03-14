from flask_cors import CORS
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure CORS with specific options
CORS(app, resources={r"/*": {"origins": "https://backend-dnxz.onrender.com"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

# Flask configuration
app.url_map.strict_slashes = False
app.config.from_pyfile('./config.py')
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db

# Register blueprints

# Login blueprint
from .login.route import login_bp
app.register_blueprint(login_bp, url_prefix='/login')

# Leave management blueprint
from .leave_management.routes import leave_management_bp
app.register_blueprint(leave_management_bp, url_prefix='/leave_management')

# PMS employee blueprint
from .pms_employee.routes import pms_employee_bp
app.register_blueprint(pms_employee_bp, url_prefix='/pms_employee')

#Employee_profile
from .employee_profile import employee_profile_bp
app.register_blueprint(employee_profile_bp, url_prefix='/employee')


#Password change
# Quicklinks - Password Change
from .quick_links.passwordchange.routes import passwordchange_bp
app.register_blueprint(passwordchange_bp, url_prefix='/quicklinks/passwordchange')

# Initialize database
with app.app_context():
    db.create_all()
