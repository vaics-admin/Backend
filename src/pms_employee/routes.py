# # src/pms_employee/routes.py
# from flask import Blueprint, request, jsonify
# from .module import save_employee_goals, submit_employee_appraisal
from datetime import datetime
import logging

# pms_employee_bp = Blueprint('pms_employee', __name__)

# @pms_employee_bp.route('/api/goals', methods=['POST'])
# def save_goals():
#     try:
#         data = request.json
#         print(data)
#         if not isinstance(data, list):
#             return jsonify({"error": "Data should be a list of goal objects"}), 400
        
#         success = save_employee_goals(data)
#         if success:
#             return jsonify({"message": "Goals saved successfully"}), 200
#         return jsonify({"error": "Failed to save goals"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @pms_employee_bp.route('/submit_appraisal', methods=['POST'])
# def submit_appraisal():
#     try:
#         data = request.json
#         if not isinstance(data, list):
#             return jsonify({"error": "Data should be a list of appraisal objects"}), 400

#         # Validate required fields
#         required_fields = [
#             "emp_id", "evaluation_date", "emp_performance_rating", 
#             "mgr_performance_rating", "goals_achieved", "feedback", 
#             "comments", "kpa", "kra", "weightage_metrics", 
#             "next_evaluation_date", "status"
#         ]

#         for appraisal in data:
#             missing_fields = [field for field in required_fields if field not in appraisal]
#             if missing_fields:
#                 return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

#         success = submit_employee_appraisal(data)
#         if success:
#             return jsonify({"message": "Appraisal submitted successfully"}), 201
#         return jsonify({"error": "Failed to submit appraisal"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# src/pms_employee/routes.py
# from flask import Blueprint, request, jsonify
# from .module import save_employee_goals, submit_employee_appraisal

# pms_employee_bp = Blueprint('pms_employee', __name__)

# def map_fields(data):
#     """Normalize field names to match the database schema."""
#     field_map = {
#         'SL. NO': 'sl_no',
#         'KRA NAME': 'kraName',
#         'KPI NAME': 'kpiName',
#         'WEIGHTAGE %': 'weightage',
#         'EMPLOYEE ID': 'empcode',
#         'MEASUREMENT METRICS': 'measurement_metrics'
#     }
#     return [
#         {field_map[key]: value for key, value in item.items() if key in field_map}
#         for item in data
#     ]

# def validate_data(data):
#     """Validate and clean data."""
#     for item in data:
#         # Ensure employee_id is present
#         if not item.get('empcode'):
#             raise ValueError("Employee ID is required")
        
#         # Convert weightage and measurement_metrics to integers
#         try:
#             item['weightage'] = int(item['weightage'])
#             item['measurement_metrics'] = int(item['measurement_metrics'])
#         except ValueError:
#             raise ValueError("Weightage and Measurement Metrics must be integers")
#     return data

# @pms_employee_bp.route('/api/goals', methods=['POST'])
# def save_goals():
#     """API endpoint to save employee goals."""
#     try:
#         # Parse the incoming JSON data
#         data = request.json
#         if not isinstance(data, list):
#             return jsonify({"error": "Data should be a list of goal objects"}), 400

#         print("Received data:", data)

#         # Normalize field names
#         normalized_data = map_fields(data)
#         print("Normalized data:", normalized_data)

#         # Validate and clean data
#         validated_data = validate_data(normalized_data)
#         print("Validated data:", validated_data)

#         # Save goals to the database
#         success = save_employee_goals(validated_data)
#         if success:
#             return jsonify({"message": "Goals saved successfully"}), 200
#         return jsonify({"error": "Failed to save goals"}), 500

#     except Exception as e:
#         print("Error occurred:", str(e))
#         return jsonify({"error": str(e)}), 500

# @pms_employee_bp.route('/submit_appraisal', methods=['POST'])
# def submit_appraisal():
#     try:
#         data = request.json
#         if not isinstance(data, list):
#             return jsonify({"error": "Data should be a list of appraisal objects"}), 400
#         success = submit_employee_appraisal(data)
#         if success:
#             return jsonify({"message": "Appraisal submitted successfully"}), 201
#         return jsonify({"error": "Failed to submit appraisal"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


################################################################################################
from flask import Blueprint, request, jsonify
from .module import save_employee_goals, submit_employee_appraisal

pms_employee_bp = Blueprint('pms_employee', __name__)

@pms_employee_bp.route('/api/goals', methods=['POST'])
def save_goals():
    try:
        data = request.get_json()  # Parsing the request body
        print(data)
        appraisal_year = "2025"  # Modify as per your logic to retrieve the year
        if not save_employee_goals(data, appraisal_year):
            raise Exception("Failed to save employee goals.")
        return jsonify({"message": "Goals submitted successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# @pms_employee_bp.route('/submit_appraisal', methods=['POST'])
# def submit_appraisal():
   
#     try:
#         data = request.get_json()  # Parsing the request body
        
#         # Extract the appraisal year (for example)
#         appraisal_year = data.get('appraisal_year')
#         if not appraisal_year:
#             raise ValueError("Appraisal year is missing")
        
#         # Extract other required fields
#         employee_name = data.get('employee_name')
#         employee_id = data.get('employee_id')
#         department = data.get('department')
#         performance_rating = data.get('performance_rating')
#         strengths = data.get('strengths')
#         areas_of_improvement = data.get('areas_of_improvement')
#         goals = data.get('goals')
#         feedback = data.get('feedback')

#         # Validate that all necessary fields are present
#         if not all([employee_name, employee_id, department, performance_rating, strengths, areas_of_improvement, goals, feedback]):
#             raise ValueError("Missing required fields")

#         # Save the appraisal data (you may have a function for this)
#         result = submit_employee_appraisal(data)
#         if not result:
#             raise Exception("Failed to save appraisal data")

#         return jsonify({"message": "Appraisal submitted successfully!"}), 200
#     except Exception as e:
#         logging.error(f"Error in submit_appraisal: {str(e)}")
#         return jsonify({"message": f"Error: {str(e)}"}), 500

@pms_employee_bp.route('/submit_appraisal', methods=['POST'])
def submit_appraisal():
    try:
        # Parsing the request body
        data = request.get_json()  # This returns a list or a dictionary
        print(data)
        # Check if data is a list or a single dictionary
        if isinstance(data, list):
            # Process the list of appraisals
            result = submit_employee_appraisal(data)
        else:
            # If it's a single appraisal, make it a list for processing
            result = submit_employee_appraisal([data])
        
        if not result:
            raise Exception("Failed to save appraisal data")
        
        return jsonify({"message": "Appraisal submitted successfully!"}), 200
    except Exception as e:
        logging.error(f"Error in submit_appraisal: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500
