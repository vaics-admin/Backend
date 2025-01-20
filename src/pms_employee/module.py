# # src/pms_employee/module.py
# from datetime import datetime
# from src.module import PmsEmployee
# from src.app import db

# def save_employee_goals(goals_data):
#     """
#     Save employee goals to the database.
#     """
#     try:
#         for goal in goals_data:
#             new_goal = PmsEmployee(
#                 emp_id=goal['emp_id'],
#                 evaluation_period=datetime.strptime(goal['evaluation_period'], '%Y-%m-%d'),
#                 emp_performance_rating=goal.get('emp_performance_rating'),
#                 mgr_performance_rating=goal.get('mgr_performance_rating'),
#                 goals_achieved=goal['goals_achieved'],
#                 feedback=goal['feedback'],
#                 evaluator_id=goal['evaluator_id'],
#                 evaluation_date=datetime.strptime(goal['evaluation_date'], '%Y-%m-%d'),
#                 next_evaluation_date=datetime.strptime(goal['next_evaluation_date'], '%Y-%m-%d') if goal.get('next_evaluation_date') else None,
#                 status=goal.get('status', 'Pending'),
#                 kpa=goal['kpa'],
#                 kra=goal['kra'],
#                 weightage_metrics=goal['weightage_metrics']
#             )
#             db.session.add(new_goal)
        
#         db.session.commit()
#         return True
#     except Exception as e:
#         db.session.rollback()
#         raise e

# def submit_employee_appraisal(appraisal_data):
#     """
#     Submit employee appraisal to the database.
#     """
#     try:
#         for appraisal in appraisal_data:
#             new_appraisal = PmsEmployee(
#                 emp_id=appraisal['emp_id'],
#                 evaluation_period=datetime.strptime(appraisal['evaluation_period'], '%Y-%m-%d'),
#                 emp_performance_rating=appraisal['emp_performance_rating'],
#                 mgr_performance_rating=appraisal['mgr_performance_rating'],
#                 goals_achieved=appraisal['goals_achieved'],
#                 feedback=appraisal['feedback'],
#                 comments=appraisal['comments'],
#                 evaluation_date=datetime.strptime(appraisal['evaluation_date'], '%Y-%m-%d'),
#                 next_evaluation_date=datetime.strptime(appraisal['next_evaluation_date'], '%Y-%m-%d'),
#                 status=appraisal['status'],
#                 kpa=appraisal['kpa'],
#                 kra=appraisal['kra'],
#                 weightage_metrics=appraisal['weightage_metrics']
#             )
#             db.session.add(new_appraisal)
        
#         db.session.commit()
#         return True
#     except Exception as e:
#         db.session.rollback()
#         raise e



# src/pms_employee/module.py
from datetime import datetime
from src.module import PmsEmployee
from src.app import db

import logging

def save_employee_goals(goals_data, appraisal_year):
    try:
        for goal in goals_data:
            new_goal = PmsEmployee(
                emp_id=goal['EMPLOYEE ID'],
                evaluation_period=datetime.strptime(appraisal_year, '%Y'),
                status='Pending',
                kpa=goal['KRA NAME'],
                kra=goal['KPI NAME'],
                weightage_metrics=goal['WEIGHTAGE %'],
            )
            db.session.add(new_goal)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while saving employee goals: {str(e)}")  # Logs error details
        raise e

def submit_employee_appraisal(appraisal_data):
    """
    Submit employee appraisal to the database.
    """
    try:
        for data in appraisal_data:
            new_appraisal = PmsEmployee(
            employee_name=data['employee_name'],  # Ensure this is passed properly
            emp_id=data['employee_id'],
            department=data['department'],
            appraisal_year=data['appraisal_year'],
            performance_rating=data['performance_rating'],
            strengths=data['strengths'],
            areas_of_improvement=data['areas_of_improvement'],
            goals=data['goals'],
            feedback=data['feedback']
        )
        db.session.add(new_appraisal)
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error saving appraisal: {str(e)}")
        return False
