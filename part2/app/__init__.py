from flask import Flask
from flask_restx import Api
from app.presentation.api.v1.users import api as users_ns
from app.presentation.api.v1.amenities import api as amenities_ns

def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        doc="/"
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")

    return app
