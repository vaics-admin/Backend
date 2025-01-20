from src.module import VaicsData

def get_user_by_empcode(empcode):
    """
    Fetch user details by empcode using SQLAlchemy.
    """
    user = VaicsData.query.filter_by(empcode=empcode).first()  # This fetches the full user object
    return user  # Return the entire user object
