from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.common.exceptions import ValidationError, ConflictError, NotFoundError

api = Namespace("places", description="Places operations")

place_in = api.model("PlaceIn", {
    "name": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenity_ids": fields.List(fields.String, required=False),
})

owner_out = api.model("OwnerOut", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
})

amenity_out = api.model("AmenityOut", {
    "id": fields.String,
    "name": fields.String,
})

review_user_out = api.model("ReviewUserOut", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
})

review_place_out = api.model("ReviewPlaceOut", {
    "id": fields.String,
    "name": fields.String,
})

review_for_place_out = api.model("ReviewForPlaceOut", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
    "user": fields.Nested(review_user_out),
    "place": fields.Nested(review_place_out),
})

place_out = api.model("PlaceOut", {
    "id": fields.String,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
    "amenity_ids": fields.List(fields.String),
    "owner": fields.Nested(owner_out),
    "amenities": fields.List(fields.Nested(amenity_out)),
})

@api.route("/")
class Places(Resource):
    @api.marshal_list_with(place_out)
    def get(self):
        return facade.list_places()

    @api.expect(place_in, validate=True)
    @api.marshal_with(place_out, code=201)
    def post(self):
        try:
            return facade.create_place(api.payload), 201
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))

@api.route("/<string:place_id>")
class PlaceById(Resource):
    @api.marshal_with(place_out)
    def get(self, place_id):
        try:
            return facade.get_place(place_id)
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(place_in, validate=False)
    @api.marshal_with(place_out)
    def put(self, place_id):
        try:
            return facade.update_place(place_id, api.payload)
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))

@api.route("/<string:place_id>/reviews")
class PlaceReviews(Resource):
    @api.marshal_list_with(review_for_place_out)
    def get(self, place_id):
        try:
            return facade.list_reviews_by_place(place_id)
        except NotFoundError as e:
            api.abort(404, str(e))
