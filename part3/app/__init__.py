"""Flask Application Factory"""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_bcrypt import Bcrypt

# Import db from models (not creating a new one)
from app.models.base_model import db

# Initialize JWT, API, and Bcrypt
jwt = JWTManager()
api = Api(version='1.0', title='HBnB API', description='A simple HBnB API')
bcrypt = Bcrypt()


def create_app(config_class):
    """
    Application Factory Pattern
    
    Args:
        config_class: Configuration class object (e.g., DevelopmentConfig, ProductionConfig, TestingConfig)
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration from config_class
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints/namespaces
    from app.presentation.api.v1 import auth_ns, users_ns, places_ns, reviews_ns, amenities_ns
    
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    
    return app

