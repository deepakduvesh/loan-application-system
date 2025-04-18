from app import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os

key = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
cipher_suite = Fernet(key)

class Applicant(db.Model):
    __tablename__ = 'applicants'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    ssn = db.Column(db.LargeBinary, nullable=False)  # Encrypted
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    employment_status = db.Column(db.String(50), nullable=False)
    annual_income = db.Column(db.Numeric(12, 2), nullable=False)
    credit_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    
    applications = db.relationship('Application', backref='applicant', lazy=True)
    
    def set_ssn(self, ssn):
        self.ssn = cipher_suite.encrypt(ssn.encode())
    
    def get_ssn(self):
        return cipher_suite.decrypt(self.ssn).decode()
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'employment_status': self.employment_status,
            'annual_income': float(self.annual_income) if self.annual_income else None,
            'credit_score': self.credit_score
        }