from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.persistence.repository import PlaceRepository, AmenityRepository, UserRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import db, Place

api = Namespace("places", description="Places operations")

place_in = api.model("PlaceIn", {
    "name": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
})

place_out = api.inherit("PlaceOut", place_in, {
    "id": fields.String,
    "owner_id": fields.String,
    "amenity_ids": fields.List(fields.String),
    "review_ids": fields.List(fields.String),
})

@api.route("/")
class Places(Resource):
    @api.marshal_list_with(place_out)
    def get(self):
        """List all places"""
        try:
            repo = PlaceRepository()
            places = repo.list_all()
            return [place.to_dict() for place in places]
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(place_in, validate=True)
    @api.marshal_with(place_out, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        try:
            current_user_id = get_jwt_identity()
            data = api.payload
            
            if not data.get('name', '').strip():
                api.abort(400, "name is required")
            if not data.get('description', '').strip():
                api.abort(400, "description is required")
            if not data.get('price'):
                api.abort(400, "price is required")
            if data['price'] < 0:
                api.abort(400, "price must be positive")
            if not data.get('latitude') or data['latitude'] < -90 or data['latitude'] > 90:
                api.abort(400, "latitude must be between -90 and 90")
            if not data.get('longitude') or data['longitude'] < -180 or data['longitude'] > 180:
                api.abort(400, "longitude must be between -180 and 180")
            
            place = Place(
                name=data['name'].strip(),
                description=data['description'].strip(),
                price=float(data['price']),
                latitude=float(data['latitude']),
                longitude=float(data['longitude']),
                owner_id=current_user_id
            )
            
            repo = PlaceRepository()
            created_place = repo.add(place)
            return created_place.to_dict(), 201
        except ConflictError as e:
            api.abort(409, str(e))
        except ValidationError as e:
            api.abort(400, str(e))

@api.route("/<string:place_id>")
class PlaceById(Resource):
    @api.marshal_with(place_out)
    def get(self, place_id):
        """Get a specific place"""
        try:
            repo = PlaceRepository()
            place = repo.get(place_id)
            return place.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(place_in, validate=False)
    @api.marshal_with(place_out)
    @jwt_required()
    def put(self, place_id):
        """Update a place"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            repo = PlaceRepository()
            place = repo.get(place_id)
            
            # Admins can update any place, non-admins can only update their own
            if place.owner_id != current_user_id and not is_admin:
                api.abort(403, "You can only update your own places")
            
            data = api.payload
            place = repo.update(place_id, data)
            return place.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            repo = PlaceRepository()
            place = repo.get(place_id)
            
            # Admins can delete any place, non-admins can only delete their own
            if place.owner_id != current_user_id and not is_admin:
                api.abort(403, "You can only delete your own places")
            
            repo.delete(place_id)
            return {"message": "Place deleted successfully"}, 200
        except NotFoundError as e:
            api.abort(404, str(e))
