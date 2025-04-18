from app import db
from sqlalchemy.sql import func
from enum import Enum

class ApplicationStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    loan_amount = db.Column(db.Numeric(12, 2), nullable=False)
    loan_purpose = db.Column(db.String(200), nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)  # in months
    application_date = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.String(20), default=ApplicationStatus.PENDING.value)
    risk_score = db.Column(db.Integer)
    officer_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'applicant_id': self.applicant_id,
            'loan_amount': float(self.loan_amount) if self.loan_amount else None,
            'loan_purpose': self.loan_purpose,
            'loan_term': self.loan_term,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status,
            'risk_score': self.risk_score,
            'officer_notes': self.officer_notes
        }