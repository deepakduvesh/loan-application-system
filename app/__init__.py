from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
from app.config import Config
from sqlalchemy.exc import OperationalError
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    with app.app_context():
        try:
            # Simple query to check DB connection
            db.session.execute(text('SELECT 1'))
            print("✅ Database connected successfully!") 
        except OperationalError as e:
            print("❌ Database connection failed:", e)
    # Register blueprints
    # from app.routes.api import api_bp
    from app.routes.views import views_bp
    # app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)

    # @app.route('/')
    # def index():
    #     return '🚀 Flask server is up and running!'
    
    return app