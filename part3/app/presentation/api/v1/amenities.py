from flask_restx import Namespace, Resource, fields
from app.persistence.repository import AmenityRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import Amenity
from app.auth.auth_utils import admin_required

api = Namespace("amenities", description="Amenities operations")

amenity_in = api.model("AmenityIn", {
    "name": fields.String(required=True),
})

amenity_out = api.inherit("AmenityOut", amenity_in, {
    "id": fields.String,
})

@api.route("/")
class Amenities(Resource):
    @api.marshal_list_with(amenity_out)
    def get(self):
        """List all amenities"""
        try:
            repo = AmenityRepository()
            amenities = repo.list_all()
            return [amenity.to_dict() for amenity in amenities]
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out, code=201)
    @admin_required
    def post(self):
        """Create a new amenity (Admin only)"""
        try:
            data = api.payload
            
            if not data.get('name', '').strip():
                api.abort(400, "name is required")
            
            repo = AmenityRepository()
            if repo.name_exists(data['name']):
                api.abort(409, "Amenity with this name already exists")
            
            amenity = Amenity(name=data['name'].strip())
            created_amenity = repo.add(amenity)
            return created_amenity.to_dict(), 201
        except ConflictError as e:
            api.abort(409, str(e))
        except ValidationError as e:
            api.abort(400, str(e))

@api.route("/<string:amenity_id>")
class AmenityById(Resource):
    @api.marshal_with(amenity_out)
    def get(self, amenity_id):
        """Get a specific amenity"""
        try:
            repo = AmenityRepository()
            amenity = repo.get(amenity_id)
            return amenity.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out)
    @admin_required
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        try:
            data = api.payload
            repo = AmenityRepository()
            amenity = repo.update(amenity_id, data)
            return amenity.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

    @admin_required
    def delete(self, amenity_id):
        """Delete an amenity (Admin only)"""
        try:
            repo = AmenityRepository()
            repo.delete(amenity_id)
            return {"message": "Amenity deleted successfully"}, 200
        except NotFoundError as e:
            api.abort(404, str(e))
