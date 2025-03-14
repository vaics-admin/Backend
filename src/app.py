import os
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
from src.login.route import login_bp
app.register_blueprint(login_bp, url_prefix='/login')

from src.leave_management.routes import leave_management_bp
app.register_blueprint(leave_management_bp, url_prefix='/leave_management')

from src.pms_employee.routes import pms_employee_bp
app.register_blueprint(pms_employee_bp, url_prefix='/pms_employee')

from src.employee_profile.routes import employee_profile_bp
app.register_blueprint(employee_profile_bp, url_prefix='/employee')

from src.quick_links.passwordchange.routes import passwordchange_bp
app.register_blueprint(passwordchange_bp, url_prefix='/quicklinks/passwordchange')

# Initialize database
with app.app_context():
    db.create_all()

# Home Route
@app.route("/")
def home():
    return "Flask App is Running Successfully on Render!"

# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Use Render's PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
