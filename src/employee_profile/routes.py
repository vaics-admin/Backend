# src/quick_links/routes.py
from flask import jsonify, request
from src.app import db
from . import employee_profile_bp
from .module import Education, Experience, LanguageDetails
from .module import parse_date, validate_date_format, calculate_years_of_experience
from src.module import VaicsData
import logging

@employee_profile_bp.route('/basic-details', methods=['POST'])
def add_basic_details():
    try:
        data = request.json
        logging.debug(f"Data received: {data}")

        # Extract sections
        employment_info = data.get('employmentInfo', {})
        reporting_structure = data.get('reportingStructure', {})
        personal_details = data.get('personalDetails', {})
        address_details = data.get('addressDetails', {})

        # Validate date fields
        for field, value in [
            ('dateOfJoining', employment_info.get('dateOfJoining')),
            ('originalBirthDate', personal_details.get('originalBirthDate')),
            ('confirmationDate', employment_info.get('confirmationDate'))
        ]:
            if value and not validate_date_format(value):
                return jsonify({'error': f'Invalid format for {field}'}), 400

        new_employee = VaicsData(
            empcode=employment_info.get('loginId'),
            name=employment_info.get('name'),
            # ... [rest of the fields]
        )

        db.session.add(new_employee)
        db.session.commit()

        return jsonify({'message': 'Employee basic details saved successfully'}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error details: {e}")
        return jsonify({'error': str(e)}), 500

@employee_profile_bp.route('/other-details', methods=['POST'])
def add_other_details():
    try:
        data = request.json
        employee_id = data.get('employee_id') or data.get('employeeId')
        
        if not employee_id:
            return jsonify({'error': 'employee_id is required'}), 400

        # Check if employee exists
        employee = VaicsData.query.get(employee_id)
        if not employee:
            return jsonify({'error': 'Invalid Employee ID'}), 400

        # Process education details
        for edu in data.get('education', []):
            education = Education(
                employee_id=employee_id,
                year_of_passing=edu.get('yearOfPassing'),
                # ... [rest of education fields]
            )
            db.session.add(education)

        # Process experience details
        for exp in data.get('experience', []):
            joining_date = parse_date(exp.get('joiningDate'))
            leaving_date = parse_date(exp.get('leavingDate'))
            years = calculate_years_of_experience(joining_date, leaving_date)
            
            experience = Experience(
                emp_id=employee_id,
                company_name=exp.get('companyName'),
                joining_date=joining_date,
                leaving_date=leaving_date,
                years_of_experience=years,
                # ... [rest of experience fields]
            )
            db.session.add(experience)

        # Process language details
        for lang in data.get('languages', []):
            language = LanguageDetails(
                employee_id=employee_id,
                language_type=lang.get('languageType'),
                can_speak=lang.get('canSpeak', False),
                can_read=lang.get('canRead', False),
                can_write=lang.get('canWrite', False)
            )
            db.session.add(language)

        db.session.commit()
        return jsonify({'message': 'Other details saved successfully'}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error details: {e}")
        return jsonify({'error': str(e)}), 500
