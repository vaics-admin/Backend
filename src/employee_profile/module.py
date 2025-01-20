from datetime import datetime
import logging

def parse_date(date_string):
    """Parse date strings into datetime objects and convert them into YYYY-MM-DD format."""
    try:
        if date_string and date_string.strip():
            date_string = date_string.strip()
            
            try:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            except ValueError:
                date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            
            return date_obj.strftime("%Y-%m-%d")
        return None
    except ValueError:
        logging.error(f"Failed to parse date: {date_string}")
        return None

def validate_date_format(date_string):
    """Validate if the date string matches the format DD-MM-YYYY or YYYY-MM-DD."""
    try:
        if date_string:
            date_string = date_string.strip()
            logging.debug(f"Validating date: {date_string}")
            
            try:
                datetime.strptime(date_string, "%d-%m-%Y")
            except ValueError:
                datetime.strptime(date_string, "%Y-%m-%d")
            
            return True
    except ValueError:
        logging.error(f"Invalid date format: {date_string}")
        return False
    return False

def calculate_years_of_experience(joining_date, leaving_date):
    """Calculate years of experience between two dates."""
    if joining_date and leaving_date:
        years = round((datetime.strptime(leaving_date, "%Y-%m-%d") - 
                      datetime.strptime(joining_date, "%Y-%m-%d")).days / 365.0, 2)
    elif joining_date:
        years = round((datetime.today().date() - 
                      datetime.strptime(joining_date, "%Y-%m-%d").date()).days / 365.0, 2)
    else:
        years = None
    return years
