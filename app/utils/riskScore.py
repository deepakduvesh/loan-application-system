class RiskScore:
    @staticmethod
    def calculate_risk_score(credit_score, annual_income, loan_amount):
        if credit_score is None or annual_income is None or loan_amount is None:
            return None

        risk_score = (loan_amount / annual_income) * 100 - (credit_score / 10)
        return max(0, min(100, round(risk_score)))