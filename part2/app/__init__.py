import os
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import config
from app.models import db

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Evolution API')

    from app.presentation.api.v1.users import api as users_ns
    from app.presentation.api.v1.amenities import api as amenities_ns
    from app.presentation.api.v1.places import api as places_ns
    from app.presentation.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return identity

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        from app.persistence.repository.database import UserRepository
        try:
            repo = UserRepository()
            user = repo.get(identity)
            return {"is_admin": user.is_admin}
        except:
            return {"is_admin": False}

    return app
