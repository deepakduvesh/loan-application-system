from flask import Blueprint, render_template, request, redirect, flash, current_app, url_for
from app.controllers.data_validation import LoanApplicationData
from app.models.applicant import Applicant
from app.models.application import Application
from app import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest

# Define the Blueprint for views
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template("base.html")

@views_bp.route('/applications/new', methods=['GET', 'POST'])
def new_application():
    if request.method == 'POST':
        try:
            data = {
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'date_of_birth': request.form.get('date_of_birth'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'zip_code': request.form.get('zip_code'),
                'employment_status': request.form.get('employment_status'),
                'annual_income': int(request.form.get('annual_income')),
                'credit_score': int(request.form.get('credit_score')),
                'loan_amount': int(request.form.get('loan_amount')),
                'loan_purpose': request.form.get('loan_purpose'),
                'loan_term': int(request.form.get('loan_term')),
            }

            # Validate application data
            try:
                LoanApplicationData.validate_application_data(data)
            except BadRequest as e:
                flash(f'Validation error: {str(e)}', 'danger')
                return render_template('application_form.html', data=data)

            # Check if applicant already exists
            applicant = Applicant.query.filter_by(email=data['email']).first()
            if not applicant:
                applicant = Applicant(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    date_of_birth=data['date_of_birth'],
                    email=data['email'],
                    phone=data['phone'],
                    address=data['address'],
                    city=data['city'],
                    state=data['state'],
                    zip_code=data['zip_code'],
                    employment_status=data['employment_status'],
                    annual_income=data['annual_income'],
                    credit_score=data['credit_score'],
                )
                db.session.add(applicant)
                db.session.flush()
            else:
                # Optionally update existing applicant's information
                applicant.first_name = data['first_name']
                applicant.last_name = data['last_name']
                applicant.phone = data['phone']
                applicant.address = data['address']
                applicant.city = data['city']
                applicant.state = data['state']
                applicant.zip_code = data['zip_code']
                applicant.employment_status = data['employment_status']
                applicant.annual_income = data['annual_income']
                applicant.credit_score = data['credit_score']
                db.session.flush()

            # Create a new loan application
            application = Application(
                applicant_id=applicant.id,
                loan_amount=data['loan_amount'],
                loan_purpose=data['loan_purpose'],
                loan_term=data['loan_term']
            )
            db.session.add(application)
            db.session.commit()

            flash('Application submitted successfully!', 'success')
            return redirect(url_for('views.application_detail', application_id=application.id))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Unexpected error: {str(e)}', 'danger')

    return render_template('application_form.html')


@views_bp.route('/applications/<int:application_id>')
def application_detail(application_id):
    application = Application.query.get_or_404(application_id)
    applicant = Applicant.query.get_or_404(application.applicant_id)
    return render_template('application_detail.html', application=application, applicant=applicant)