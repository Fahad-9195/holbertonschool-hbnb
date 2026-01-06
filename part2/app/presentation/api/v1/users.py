from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.common.exceptions import ValidationError, ConflictError, NotFoundError

api = Namespace("users", description="Users operations")

user_in = api.model("UserIn", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
})

user_out = api.inherit("UserOut", user_in, {
    "id": fields.String,
})

@api.route("/")
class Users(Resource):
    @api.marshal_list_with(user_out)
    def get(self):
        return facade.list_users()

    @api.expect(user_in, validate=True)
    @api.marshal_with(user_out, code=201)
    def post(self):
        try:
            return facade.create_user(api.payload), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except ConflictError as e:
            api.abort(409, str(e))

@api.route("/<string:user_id>")
class UserById(Resource):
    @api.marshal_with(user_out)
    def get(self, user_id):
        try:
            return facade.get_user(user_id)
        except NotFoundError as e:
            api.abort(404, str(e))
