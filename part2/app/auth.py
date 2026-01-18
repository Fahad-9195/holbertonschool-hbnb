from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from functools import wraps
import bcrypt
from datetime import timedelta

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    if isinstance(password, str):
        password = password.encode('utf-8')
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(password, hashed)

def generate_token(user_id: str, expires_delta: timedelta = None) -> str:
    """Generate a JWT token for a user"""
    if expires_delta:
        return create_access_token(identity=user_id, expires_delta=expires_delta)
    else:
        return create_access_token(identity=user_id)

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """Get the current authenticated user ID"""
    return get_jwt_identity()
