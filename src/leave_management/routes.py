# src/leave_management/routes.py
import datetime
from flask import Blueprint, request, jsonify
from .module import calculate_working_days, get_leave_balance, manage_leave_request
from .module import LeaveRequest, LeaveBalance
from src.app import db

leave_management_bp = Blueprint('leave_management', __name__)

# Route to add a leave request
@leave_management_bp.route('/addleaverequest', methods=['POST'])
def add_leave_request():
    
    data = request.json
    print(data)
    emp_id = data.get("employee_id")
    print(emp_id)
    leave_type = data.get("leaveType")
    print(leave_type)
    from_date = data.get("fromDate")
    print(from_date)
    to_date = data.get("toDate")
    print(to_date)
    reason = data.get("reason")
    print(reason)

    if not all([emp_id, leave_type, from_date, to_date, reason]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Calculate the number of leave days
        from_date_obj = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
        no_of_days = calculate_working_days(from_date_obj, to_date_obj)

        new_request = LeaveRequest(
            emp_id=emp_id,
            leave_type=leave_type,
            from_date=from_date_obj,
            to_date=to_date_obj,
            no_of_day=no_of_days,
            reason=reason
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message": "Leave request added successfully", "request_id": new_request.request_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get leave requests
@leave_management_bp.route('/getleaverequests', methods=['GET'])
def get_leave_requests():
    try:
        leave_requests = LeaveRequest.query.filter_by(status='Pending').order_by(LeaveRequest.applied_on.desc()).all()

        leave_requests_list = [
            {
                "request_id": request.request_id,
                "emp_id": request.emp_id,
                "leave_type": request.leave_type,
                "applied_on": request.applied_on.strftime('%Y-%m-%d'),
                "from_date": request.from_date.strftime('%Y-%m-%d'),
                "to_date": request.to_date.strftime('%Y-%m-%d'),
                "no_of_days": float(request.no_of_day) if request.no_of_day else 0,
                "reason": request.reason,
                "status": request.status,
                "approved_by": request.approved_by,
                "approved_on": request.approved_on.strftime('%Y-%m-%d') if request.approved_on else None
            } for request in leave_requests
        ]

        return jsonify(leave_requests_list), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


# # Route to manage leave requests (approve or reject)
# @leave_management_bp.route('/admin/requestmanagement', methods=['POST'])
# def manage_leave_request_route():
#     data = request.json
#     print(data)
#     required_fields = ["request_id", "status", "approved_by"]
#     for field in required_fields:
#         if field not in data:
#             return jsonify({"error": f"Missing field: {field}"}), 400

#     try:
#         # Manage leave request (approve/reject)
#         request_id = data.get("request_id")
#         status = data.get("status")
#         approved_by = data.get("approved_by")
        
#         response = manage_leave_request(request_id, status, approved_by)
#         if response:
#             return jsonify({"message": "Leave request updated successfully."}), 200
#         else:
#             return jsonify({"message": "Leave request not found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500




@leave_management_bp.route('/admin/requestmanagement', methods=['POST'])
def manage_leave_request_route():
    data = request.json
    print(data)
    
    # Map incoming payload fields to expected fields
    required_fields = ["emp_id", "is_approved", "approved_by"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # Extract and map fields
        request_id = data.get("emp_id")  # Assuming emp_id is used as request_id
        status = data.get("is_approved")  # Assuming is_approved maps to status
        approved_by = data.get("approved_by")
        
        if not request_id:
            return jsonify({"error": "Employee ID (request_id) cannot be null"}), 400
        if not status:
            return jsonify({"error": "Status cannot be null"}), 400

        # Call the leave request management logic
        response = manage_leave_request(request_id, status, approved_by)
        if response:
            return jsonify({"message": "Leave request updated successfully."}), 200
        else:
            return jsonify({"message": "Leave request not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get leave balance for an employee
@leave_management_bp.route('/get-leave-balance', methods=['POST'])
def get_leave_balance_route():
    try:
        data = request.get_json()
        emp_id = data.get('employee_id')

        if not emp_id:
            return jsonify({"error": "Employee ID is required."}), 400

        leave_balance = LeaveBalance.query.filter_by(emp_id=emp_id, year=datetime.datetime.now().year).first()

        if leave_balance:
            response_data = {
                "earned_leave": {
                    "credited": leave_balance.el_credited,
                    "carried_over": leave_balance.el_carried,
                    "availed": leave_balance.el_availed,
                    "balance": leave_balance.el_balance
                },
                "loss_of_pay": {
                    "availed": leave_balance.lop_used
                }
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "No leave balance found for the given Employee ID or year."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get an employee's leave history
@leave_management_bp.route('/employee/getleave', methods=['POST'])
def get_leave_history():
    try:
        data = request.json
        emp_id = data.get("employee_id")

        if not emp_id:
            return jsonify({"error": "Missing emp_id in request body"}), 400

        leave_history = LeaveRequest.query.filter_by(emp_id=emp_id).order_by(LeaveRequest.applied_on.desc()).all()

        if leave_history:
            history_list = [
                {
                    "request_id": leave.request_id,
                    "leave_type": leave.leave_type,
                    "from_date": leave.from_date.strftime('%Y-%m-%d'),
                    "to_date": leave.to_date.strftime('%Y-%m-%d'),
                    "no_of_day": leave.no_of_day,
                    "status": leave.status,
                    "reason": leave.reason,
                    "applied_on": leave.applied_on.strftime('%Y-%m-%d'),
                    "approved_on": leave.approved_on.strftime('%Y-%m-%d') if leave.approved_on else None,
                    "approved_by": leave.approved_by
                } for leave in leave_history
            ]
            return jsonify(history_list), 200
        else:
            return jsonify({"message": "No leave history found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500