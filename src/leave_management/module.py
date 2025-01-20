# src/leave_management/module.py
from src.module import LeaveRequest, LeaveBalance
from src.app import db

from datetime import datetime, timedelta

def calculate_working_days(from_date, to_date):
    current_date = from_date
    end_date = to_date
    working_days = 0
    while current_date <= end_date:
        if current_date.weekday() not in (5, 6):  # Skip Saturday (5) and Sunday (6)
            working_days += 1
        current_date += timedelta(days=1)
    return working_days

def get_leave_balance(emp_id):
    leave_balance = LeaveBalance.query.filter_by(emp_id=emp_id, year=datetime.now().year).first()
    if leave_balance:
        return {
            "emp_id": leave_balance.emp_id,
            "el_credited": leave_balance.el_credited,
            "el_carried": leave_balance.el_carried,
            "el_availed": leave_balance.el_availed,
            "el_balance": leave_balance.el_balance,
            "lop_used": leave_balance.lop_used
        }
    return None

def manage_leave_request(request_id, status, approved_by):
    leave_request = LeaveRequest.query.get(request_id)
    if leave_request:
        leave_request.status = status
        leave_request.approved_by = approved_by
        leave_request.approved_on = datetime.now() if status == "Approved" else None
        db.session.commit()

        # Update the leave balance if the request is approved
        if status == "Approved":
            leave_balance = LeaveBalance.query.filter_by(emp_id=leave_request.emp_id, year=datetime.now().year).first()
            if not leave_balance:
                leave_balance = LeaveBalance(
                    emp_id=leave_request.emp_id,
                    year=datetime.now().year,
                    el_credited=0,
                    el_carried=0,
                    el_availed=0,
                    el_balance=0
                )

            leave_balance.el_availed += leave_request.no_of_day
            leave_balance.el_balance -= leave_request.no_of_day
            db.session.add(leave_balance)

        db.session.commit()
        return True
    return False
