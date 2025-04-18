import re
from datetime import datetime
from werkzeug.exceptions import BadRequest

class LoanApplicationData:
    @staticmethod
    def validate_application_data(data):
        errors = []

        
        if not data.get("first_name") or not data["first_name"].isalpha():
            errors.append("Invalid first name. It must be alphabetic and non-empty.")
        if not data.get("last_name") or not data["last_name"].isalpha():
            errors.append("Invalid last name. It must be alphabetic and non-empty.")

        
        try:
            dob = datetime.strptime(data.get("date_of_birth", ""), "%Y-%m-%d")
            age = (datetime.now() - dob).days // 365
            if not (18 <= age <= 65):
                errors.append("Invalid date of birth. Age must be between 18 and 65.")
        except ValueError:
            errors.append("Invalid date of birth. Use the format YYYY-MM-DD.")

        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not data.get("email") or not re.match(email_regex, data["email"]):
            errors.append("Invalid email address.")

        
        if not data.get("phone") or not data["phone"].isdigit() or len(data["phone"]) != 10:
            errors.append("Invalid phone number. It must be 10 digits.")

        
        if not data.get("address"):
            errors.append("Address cannot be empty.")
        if not data.get("city"):
            errors.append("City cannot be empty.")
        if not data.get("state"):
            errors.append("State cannot be empty.")
        if not data.get("zip_code") or not data["zip_code"].isdigit():
            errors.append("Invalid zip code. It must be numeric.")

        
        if not data.get("employment_status"):
            errors.append("Employment status cannot be empty.")

        
        if not data.get("annual_income") or not isinstance(data["annual_income"], (int, float)) or data["annual_income"] <= 0:
            errors.append("Invalid annual income. It must be a positive number.")

        
        if not data.get("credit_score") or not isinstance(data["credit_score"], int) or not (300 <= data["credit_score"] <= 850):
            errors.append("Invalid credit score. It must be between 300 and 850.")

        
        if not data.get("loan_amount") or not isinstance(data["loan_amount"], (int, float)) or data["loan_amount"] <= 0:
            errors.append("Invalid loan amount. It must be a positive number.")

        
        if not data.get("loan_purpose"):
            errors.append("Loan purpose cannot be empty.")

        
        if not data.get("loan_term") or not isinstance(data["loan_term"], int) or data["loan_term"] <= 0:
            errors.append("Invalid loan term. It must be a positive integer.")

        if errors:
            raise BadRequest(description={"errors": errors})
        return True