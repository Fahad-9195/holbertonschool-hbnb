from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.common.exceptions import ValidationError, ConflictError, NotFoundError

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
        return facade.list_amenities()

    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out, code=201)
    def post(self):
        try:
            return facade.create_amenity(api.payload), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except ValueError as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

@api.route("/<string:amenity_id>")
class AmenityById(Resource):
    @api.marshal_with(amenity_out)
    def get(self, amenity_id):
        try:
            return facade.get_amenity(amenity_id)
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(amenity_in, validate=True)
    @api.marshal_with(amenity_out)
    def put(self, amenity_id):
        try:
            return facade.update_amenity(amenity_id, api.payload)
        except ValidationError as e:
            api.abort(400, str(e))
        except ValueError as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
