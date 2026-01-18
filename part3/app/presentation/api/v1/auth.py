from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
from app.auth.auth_utils import hash_password, verify_password
from app.persistence.repository import UserRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import db, User

api = Namespace("auth", description="Authentication operations")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

register_model = api.model("Register", {
    "first_name": fields.String(required=True, description="First name"),
    "last_name": fields.String(required=True, description="Last name"),
    "email": fields.String(required=True, description="Email address"),
    "password": fields.String(required=True, description="Password"),
})

token_response = api.model("TokenResponse", {
    "access_token": fields.String(description="JWT access token"),
    "user_id": fields.String(description="User ID"),
})

@api.route("/register")
class Register(Resource):
    @api.expect(register_model, validate=True)
    @api.marshal_with(token_response, code=201)
    def post(self):
        """Register a new user"""
        try:
            data = api.payload
            
            # Validate input
            if not data.get('first_name', '').strip():
                api.abort(400, "first_name is required")
            if not data.get('last_name', '').strip():
                api.abort(400, "last_name is required")
            if not data.get('email', '').strip():
                api.abort(400, "email is required")
            if not data.get('password', '').strip():
                api.abort(400, "password is required")
            
            # Check if email already exists
            repo = UserRepository()
            if repo.email_exists(data['email']):
                api.abort(409, "Email already registered")
            
            # Create new user
            user = User(
                first_name=data['first_name'].strip(),
                last_name=data['last_name'].strip(),
                email=data['email'].strip().lower(),
                is_admin=False
            )
            
            # Hash the password using User model's method
            user.hash_password(data['password'].strip())
            
            repo.add(user)
            
            # Generate JWT token with is_admin claim
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"is_admin": user.is_admin}
            )
            
            return {
                "access_token": access_token,
                "user_id": user.id,
            }, 201
        except ConflictError as e:
            api.abort(409, str(e))
        except ValidationError as e:
            api.abort(400, str(e))

@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(token_response, code=200)
    def post(self):
        """Login user and get JWT token"""
        try:
            data = api.payload
            
            if not data.get('email'):
                api.abort(400, "email is required")
            if not data.get('password'):
                api.abort(400, "password is required")
            
            repo = UserRepository()
            try:
                # Step 1: Retrieve the user by email
                user = repo.get_by_email(data['email'].lower())
            except NotFoundError:
                api.abort(401, "Invalid email or password")
            
            # Step 2: Verify the password
            if not user.verify_password(data['password']):
                api.abort(401, "Invalid email or password")
            
            # Step 3: Generate JWT token with is_admin claim
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"is_admin": user.is_admin}
            )
            
            # Step 4: Return the token
            return {
                "access_token": access_token,
                "user_id": user.id,
            }, 200
        except Exception as e:
            api.abort(500, str(e))
