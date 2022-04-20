from flask import g
from flask_restful import Resource
from App.apis.movie_user.utils import required, require_permission
from App.models.movie_user.movie_user_model import VIP_SUER


class MovieOrdersResource(Resource):
    @required
    def post(self):
        user = g.user
        print(user.username)
        return {"msg": "post order ok"}


class MovieOrderResource(Resource):
    @require_permission(VIP_SUER)
    def put(self, order_id):
        return {"msg": "修改成功"}
