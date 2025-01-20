#src/module.py 

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import date
from .app import db
from sqlalchemy import Column, String
from datetime import datetime, timedelta


# Define the vaics_data table model
class VaicsData(db.Model):
    __tablename__ = 'vaics_data'
    
    sl_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empcode = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    department = db.Column(db.String(255))
    division = db.Column(db.String(255))
    designation = db.Column(db.String(255))
    category = db.Column(db.String(255))
    grade = db.Column(db.String(255))
    grade_level = db.Column(db.String(255))
    emp_status = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    first_approver_code = db.Column(db.Integer)
    first_approver_name = db.Column(db.String(255))
    second_approver_code = db.Column(db.Integer)
    second_approver_name = db.Column(db.String(255))
    base_shift = db.Column(db.String(255))
    attendance_group = db.Column(db.String(255))
    weekoff_code = db.Column(db.String(255))
    fixed_shift = db.Column(db.Boolean)
    holiday_calendar = db.Column(db.String(255))
    leave_group = db.Column(db.String(255))
    co_group = db.Column(db.String(255))
    title = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    role = db.Column(db.String(255))
    login_id = db.Column(db.Integer, unique=True)
    joining_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)
    confirmation_date = db.Column(db.Date)
    last_working_date = db.Column(db.Date)
    import_map_code = db.Column(db.String(255))
    aadhaar_no = db.Column(db.BigInteger, unique=True)
    official_mail = db.Column(db.String(255))
    official_phone_no = db.Column(db.Numeric)
    exp_inside_comp = db.Column(db.String(255))
    exp_outside_company = db.Column(db.String(255))
    tot_experience = db.Column(db.String(255))
    personal_phone_no = db.Column(db.Numeric)
    personal_mailid = db.Column(db.String(255))
    blood_group = db.Column(db.String(255))
    religion = db.Column(db.String(255))
    mother_tounge = db.Column(db.String(255))
    nationality = db.Column(db.String(255))
    marital_status = db.Column(db.String(255))
    original_birth_date = db.Column(db.Date)
    place_of_birth = db.Column(db.String(255))
    age = db.Column(db.String(255))
    weight = db.Column(db.String(255))
    height = db.Column(db.String(255))
    passport_no = db.Column(db.String(255), unique=True)
    first_name_in_passport = db.Column(db.String(255))
    middle_name_in_passport = db.Column(db.String(255))
    last_name_in_passport = db.Column(db.String(255))
    passport_issue_place = db.Column(db.String(255))
    passport_issue_date = db.Column(db.Date)
    passport_expiry_date = db.Column(db.Date)
    highest_education = db.Column(db.String(255))
    highest_education_passed_year = db.Column(db.String(255))
    pan_no = db.Column(db.String(255), unique=True)
    pt_state = db.Column(db.String(255))
    emgcont_name1 = db.Column(db.String(255))
    emgcont_relationship1 = db.Column(db.String(255))
    emgcont_address1 = db.Column(db.String(255))
    emgcont_city1 = db.Column(db.String(255))
    emgcont_state1 = db.Column(db.String(255))
    emgcont_country1 = db.Column(db.String(255))
    emgcont_pincode1 = db.Column(db.Numeric)
    emgcont_contact1 = db.Column(db.Numeric)
    emgcont_name2 = db.Column(db.String(255))
    emgcont_relationship2 = db.Column(db.String(255))
    emgcont_address2 = db.Column(db.String(255))
    emgcont_city2 = db.Column(db.String(255))
    emgcont_state2 = db.Column(db.String(255))
    emgcont_country2 = db.Column(db.String(255))
    emgcont_pincode2 = db.Column(db.Numeric)
    emgcont_contact2 = db.Column(db.Numeric)
    permanent_address = db.Column(db.String(255))
    permanent_address_city = db.Column(db.String(255))
    permanent_address_state = db.Column(db.String(255))
    permanent_address_country = db.Column(db.String(255))
    permanent_address_pincode = db.Column(db.String(255))
    current_address = db.Column(db.String(255))
    current_address_city = db.Column(db.String(255))
    current_address_state = db.Column(db.String(255))
    current_address_country = db.Column(db.String(255))
    current_address_pincode = db.Column(db.Numeric)
    father_name = db.Column(db.String(255))
    mother_name = db.Column(db.String(255))
    profile_picture = db.Column(db.LargeBinary)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<VaicsData {self.name}, {self.empcode}>"

    @staticmethod
    def hash_password(plain_password):
        """
        Hash a plain password using bcrypt.
        """
        from bcrypt import hashpw, gensalt
        return hashpw(plain_password.encode(), gensalt())

    def check_password(self, plain_password):
        """
        Check a plain password against the hashed password.
        """
        from bcrypt import checkpw
        return checkpw(plain_password.encode(), self.password.encode())


################################################################################################

class LeaveRequest(db.Model):
    __tablename__ = 'leave_request'

    request_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'), nullable=False)  # Foreign key definition
    leave_type = db.Column(db.String(255), nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    no_of_day = db.Column(db.Float)
    reason = db.Column(db.String(255))
    applied_on = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(255), default='Pending')
    approved_by = db.Column(db.Integer, nullable=True)
    approved_on = db.Column(db.Date, nullable=True)

    # Establish relationship with VaicsData (optional, for easier access to employee data)
    employee = db.relationship('VaicsData', backref='leave_requests', lazy=True)

    def __repr__(self):
        return f"<LeaveRequest {self.request_id}>"

class LeaveBalance(db.Model):
    __tablename__ = 'leave_balance'

    leave_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'), nullable=False)  # Foreign key definition
    el_credited = db.Column(db.Float, default=0.0)  # Earned leave credited in the year
    el_carried = db.Column(db.Float, default=0.0)   # Earned leave carried over
    el_availed = db.Column(db.Float, default=0.0)   # Earned leave availed
    el_balance = db.Column(db.Float, default=0.0)   # Remaining earned leave balance
    lop_used = db.Column(db.Float, default=0.0)     # Leave without pay (LOP) days used
    year = db.Column(db.Integer, nullable=False)    # The year for the leave balance

    # Establish relationship with VaicsData (optional)
    employee = db.relationship('VaicsData', backref='leave_balances', lazy=True)

    def __repr__(self):
        return f"<LeaveBalance {self.leave_id}>"
    
####################################################################################


class PmsEmployee(db.Model):
    __tablename__ = 'pms_employee'

    pms_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment primary key
    emp_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'), nullable=False)  # Foreign key referencing empcode in vaics_data
    employee_name = db.Column(db.String(250))  # Make sure this is defined
    department = db.Column(db.String(255))  # Add department column
    appraisal_year = db.Column(db.String(255))  # Add appraisal_year column
    performance_rating = db.Column(db.String(255))  # Add performance_rating column
    strengths = db.Column(db.String(255))  # Add strengths column
    areas_of_improvement = db.Column(db.String(255))  # Add areas_of_improvement column
    goals = db.Column(db.String(255))  # Column name should be 'goals'

    evaluation_period = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    emp_performance_rating = db.Column(db.String(255))
    mgr_performance_rating = db.Column(db.String(255))
    goals_achieved = db.Column(db.String(255))
    feedback = db.Column(db.String(255))
    comments = db.Column(db.Text)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'), nullable=True)  # Foreign key referencing evaluator empcode
    evaluation_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    next_evaluation_date = db.Column(db.Date)
    status = db.Column(db.String(255), default='Pending')
    kpa = db.Column(db.String(255))
    kra = db.Column(db.String(255))
    weightage_metrics = db.Column(db.String(255))

    # Establish relationships
    employee = db.relationship('VaicsData', foreign_keys=[emp_id], backref='pms_employee', lazy=True)
    evaluator = db.relationship('VaicsData', foreign_keys=[evaluator_id], backref='evaluations', lazy=True)
    
    def __repr__(self):
        return f"<PmsEmployee {self.pms_id}>"

    @property
    def is_completed(self):
        """Check if the evaluation is completed."""
        return self.status.lower() == 'completed'

    @property
    def is_pending(self):
        """Check if the evaluation is pending."""
        return self.status.lower() == 'pending'

    def update_status(self, new_status):
        """Update the evaluation status."""
        self.status = new_status
        return True
    
    ########################################################################

class Education(db.Model):
    __tablename__ = 'education'
    
    education_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'))
    year_of_passing = db.Column(db.Integer)
    course_class = db.Column(db.String(255))
    institution = db.Column(db.String(255))
    grade_percent = db.Column(db.String(255))
    course_type = db.Column(db.String(255))
    board_university = db.Column(db.String(255))
    specialization = db.Column(db.String(255))
    registration_no = db.Column(db.String(255))
    doctype = db.Column(db.LargeBinary)

    employee = db.relationship('VaicsData', backref='education_details', lazy=True)

    def __repr__(self):
        return f"<Education {self.education_id}>"

class Experience(db.Model):
    __tablename__ = 'experience'
    
    experience_id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'))
    company_name = db.Column(db.String(255))
    joining_date = db.Column(db.Date)
    leaving_date = db.Column(db.Date)
    years_of_experience = db.Column(db.Float)
    skill_profile_department = db.Column(db.String(255))
    leaving_reason = db.Column(db.String(255))
    position_while_joining = db.Column(db.String(255))
    position_while_leaving = db.Column(db.String(255))
    annual_ctc = db.Column(db.Numeric)
    company_contact = db.Column(db.String(255))
    company_address = db.Column(db.String(255))

    employee = db.relationship('VaicsData', backref='experiences', lazy=True)

    def __repr__(self):
        return f"<Experience {self.experience_id}>"

class LanguageDetails(db.Model):
    __tablename__ = 'language_details'
    
    language_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('vaics_data.empcode'))
    language_type = db.Column(db.String(255), nullable=False)
    can_speak = db.Column(db.Boolean, default=False)
    can_read = db.Column(db.Boolean, default=False)
    can_write = db.Column(db.Boolean, default=False)

    employee = db.relationship('VaicsData', backref='language_details', lazy=True)

    def __repr__(self):
        return f"<LanguageDetails {self.language_id}>"