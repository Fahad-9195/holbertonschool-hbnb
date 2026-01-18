from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.persistence.repository import UserRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import db, User

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
    def post(self):
        """Create a new user"""
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
            
            user = User(
                first_name=data['first_name'].strip(),
                last_name=data['last_name'].strip(),
                email=data['email'].strip().lower(),
                is_admin=False
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
            repo = UserRepository()
            
            current_user = repo.get(current_user_id)
            if user_id != current_user_id and not current_user.is_admin:
                api.abort(403, "You can only update your own profile")
            
            data = api.payload
            user = repo.get(user_id)
            
            # Only allow updating first_name and last_name
            update_data = {}
            if 'first_name' in data:
                update_data['first_name'] = data['first_name'].strip()
            if 'last_name' in data:
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
