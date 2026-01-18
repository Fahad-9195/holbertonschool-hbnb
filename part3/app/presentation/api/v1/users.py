from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.persistence.repository import UserRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import db, User
from app.auth.auth_utils import admin_required

api = Namespace("users", description="Users operations")

user_in = api.model("UserIn", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

user_out = api.model("UserOut", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
})

@api.route("/")
class Users(Resource):
    @api.marshal_list_with(user_out)
    def get(self):
        """List all users"""
        try:
            repo = UserRepository()
            users = repo.list_all()
            return [user.to_dict() for user in users]
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(user_in, validate=True)
    @api.marshal_with(user_out, code=201)
    @admin_required
    def post(self):
        """Create a new user (Admin only)"""
        try:
            data = api.payload
            
            if not data.get('first_name', '').strip():
                api.abort(400, "first_name is required")
            if not data.get('last_name', '').strip():
                api.abort(400, "last_name is required")
            if not data.get('email', '').strip():
                api.abort(400, "email is required")
            if not data.get('password', '').strip():
                api.abort(400, "password is required")
            
            repo = UserRepository()
            if repo.email_exists(data['email']):
                api.abort(409, "Email already exists")
            
            # Admin can optionally set is_admin flag for new users
            is_admin = data.get('is_admin', False) if isinstance(data.get('is_admin'), bool) else False
            
            user = User(
                first_name=data['first_name'].strip(),
                last_name=data['last_name'].strip(),
                email=data['email'].strip().lower(),
                is_admin=is_admin
            )
            
            # Hash the password using the User model's method
            user.hash_password(data['password'].strip())
            
            created_user = repo.add(user)
            return created_user.to_dict(), 201
        except ConflictError as e:
            api.abort(409, str(e))
        except ValidationError as e:
            api.abort(400, str(e))

@api.route("/<string:user_id>")
class UserById(Resource):
    @api.marshal_with(user_out)
    def get(self, user_id):
        """Get a specific user"""
        try:
            repo = UserRepository()
            user = repo.get(user_id)
            return user.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(user_in, validate=False)
    @api.marshal_with(user_out)
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            repo = UserRepository()
            user = repo.get(user_id)
            data = api.payload
            
            # Non-admin users can only update their own profile
            if user_id != current_user_id and not is_admin:
                api.abort(403, "You can only update your own profile")
            
            # Admins can update any field (first_name, last_name, email, password, is_admin)
            # Non-admins can only update first_name and last_name
            update_data = {}
            
            if is_admin:
                # Admins can update all fields
                if 'first_name' in data and data['first_name']:
                    update_data['first_name'] = data['first_name'].strip()
                if 'last_name' in data and data['last_name']:
                    update_data['last_name'] = data['last_name'].strip()
                if 'email' in data and data['email']:
                    new_email = data['email'].strip().lower()
                    # Check if email is already in use by another user
                    existing_user = repo.get_by_email(new_email)
                    if existing_user and existing_user.id != user_id:
                        api.abort(409, "Email already exists")
                    update_data['email'] = new_email
                if 'password' in data and data['password']:
                    # Admin is setting password directly
                    update_data['password'] = data['password'].strip()
                if 'is_admin' in data and isinstance(data['is_admin'], bool):
                    update_data['is_admin'] = data['is_admin']
            else:
                # Non-admin users can only update first_name and last_name
                if 'first_name' in data and data['first_name']:
                    update_data['first_name'] = data['first_name'].strip()
                if 'last_name' in data and data['last_name']:
                    update_data['last_name'] = data['last_name'].strip()
            
            user = repo.update(user_id, update_data)
            return user.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        try:
            current_user_id = get_jwt_identity()
            repo = UserRepository()
            current_user = repo.get(current_user_id)
            
            if user_id != current_user_id and not current_user.is_admin:
                api.abort(403, "You can only delete your own profile")
            
            repo.delete(user_id)
            return {"message": "User deleted successfully"}, 200
        except NotFoundError as e:
            api.abort(404, str(e))
