from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.persistence.repository import ReviewRepository, UserRepository, PlaceRepository, ConflictError, NotFoundError, ValidationError
from app.models.base_model import db, Review

api = Namespace("reviews", description="Reviews operations")

review_in = api.model("ReviewIn", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "place_id": fields.String(required=True),
})

review_out = api.model("ReviewOut", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
})

@api.route("/")
class Reviews(Resource):
    @api.marshal_list_with(review_out)
    def get(self):
        """List all reviews"""
        try:
            repo = ReviewRepository()
            reviews = repo.list_all()
            return [review.to_dict() for review in reviews]
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(review_in, validate=True)
    @api.marshal_with(review_out, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""
        try:
            current_user_id = get_jwt_identity()
            data = api.payload
            
            if not data.get('text', '').strip():
                api.abort(400, "text is required")
            if not data.get('rating'):
                api.abort(400, "rating is required")
            if not data.get('place_id'):
                api.abort(400, "place_id is required")
            
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                api.abort(400, "rating must be between 1 and 5")
            
            # Get the place
            place_repo = PlaceRepository()
            try:
                place = place_repo.get(data['place_id'])
            except NotFoundError:
                api.abort(404, "Place not found")
            
            # Check if user owns the place
            if place.owner_id == current_user_id:
                api.abort(400, "You cannot review your own place")
            
            # Check if user has already reviewed this place
            review_repo = ReviewRepository()
            if review_repo.user_has_reviewed_place(current_user_id, data['place_id']):
                api.abort(400, "You have already reviewed this place")
            
            review = Review(
                text=data['text'].strip(),
                rating=rating,
                user_id=current_user_id,
                place_id=data['place_id']
            )
            
            created_review = review_repo.add(review)
            return created_review.to_dict(), 201
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

@api.route("/<string:review_id>")
class ReviewById(Resource):
    @api.marshal_with(review_out)
    def get(self, review_id):
        """Get a specific review"""
        try:
            repo = ReviewRepository()
            review = repo.get(review_id)
            return review.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))

    @api.expect(review_in, validate=False)
    @api.marshal_with(review_out)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        try:
            current_user_id = get_jwt_identity()
            repo = ReviewRepository()
            review = repo.get(review_id)
            
            user_repo = UserRepository()
            current_user = user_repo.get(current_user_id)
            
            if review.user_id != current_user_id and not current_user.is_admin:
                api.abort(403, "You can only update your own reviews")
            
            data = api.payload
            
            if 'text' in data and data['text']:
                review.text = data['text'].strip()
            if 'rating' in data and data['rating'] is not None:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    api.abort(400, "rating must be between 1 and 5")
                review.rating = rating
            
            db.session.commit()
            return review.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except (ValidationError, ValueError) as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        try:
            current_user_id = get_jwt_identity()
            repo = ReviewRepository()
            review = repo.get(review_id)
            
            user_repo = UserRepository()
            current_user = user_repo.get(current_user_id)
            
            if review.user_id != current_user_id and not current_user.is_admin:
                api.abort(403, "You can only delete your own reviews")
            
            repo.delete(review_id)
            return {"message": "Review deleted successfully"}, 200
        except NotFoundError as e:
            api.abort(404, str(e))
