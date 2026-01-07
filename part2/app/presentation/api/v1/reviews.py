from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.common.exceptions import ValidationError, ConflictError, NotFoundError

api = Namespace("reviews", description="Reviews operations")

review_in = api.model("ReviewIn", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
})

user_out = api.model("UserOut", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
})

place_out = api.model("PlaceOut", {
    "id": fields.String,
    "name": fields.String,
})

review_out = api.model("ReviewOut", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
    "user": fields.Nested(user_out),
    "place": fields.Nested(place_out),
})

@api.route("/")
class Reviews(Resource):
    @api.marshal_list_with(review_out)
    def get(self):
        return facade.list_reviews()

    @api.expect(review_in, validate=True)
    @api.marshal_with(review_out, code=201)
    def post(self):
        try:
            return facade.create_review(api.payload), 201
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))

@api.route("/<string:review_id>")
class ReviewById(Resource):
    @api.marshal_with(review_out)
    def get(self, review_id):
        try:
            return facade.get_review(review_id)
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(review_in, validate=False)
    @api.marshal_with(review_out)
    def put(self, review_id):
        try:
            return facade.update_review(review_id, api.payload)
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.doc(responses={200: "Review deleted successfully", 404: "Review not found"})
    def delete(self, review_id):
        try:
            return facade.delete_review(review_id), 200
        except NotFoundError as e:
            api.abort(404, str(e))
