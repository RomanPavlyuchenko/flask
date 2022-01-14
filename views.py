from flask import jsonify, request
from flask.views import MethodView

import errors
from app import app
from validator import validate
from models import User, Advertisement
from schema import USER_CREATE, ADV_CREATE


class UserView(MethodView):

    def get(self, user_id):
        user = User.get(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        token = user.set_token()
        user.add()
        response = user.to_dict()
        response['token'] = token
        return jsonify(response)


class AdvertisementView(MethodView):

    def get(self, adv_id):
        adv = Advertisement.get(adv_id)
        return jsonify(adv.to_dict())

    @validate('json', ADV_CREATE)
    def post(self):
        try:
            if User.verify_user(
                request.json['username'],
                request.headers['Authorization']
            ):
                adv = Advertisement(
                    owner_id=User.get_by_name(username=request.json.pop('username')).id,
                    **request.json
                )
                adv.add()
                return jsonify(adv.to_dict())
            else:
                raise errors.Forbidden
        except Exception as msg:
            print(msg)

    def delete(self, adv_id):
        if not User.verify_user(
                request.json['username'],
                request.headers['Authorization']
        ):
            raise errors.AuthError

        adv = Advertisement.get(adv_id)
        if adv.owner.username == request.json['username']:
            data = jsonify(adv.to_dict())
            adv.delete()
            return data
        else:
            raise errors.Forbidden


app.add_url_rule(
    '/users/<int:user_id>',
    view_func=UserView.as_view('users_get'),
    methods=['GET', ]
)
app.add_url_rule(
    '/users/',
    view_func=UserView.as_view('users_create'),
    methods=['POST', ]
)

app.add_url_rule(
    '/adv/<int:adv_id>',
    view_func=AdvertisementView.as_view('advertisements_get'),
    methods=['GET', ]
)
app.add_url_rule(
    '/adv/<int:adv_id>',
    view_func=AdvertisementView.as_view('advertisements_delete'),
    methods=['DELETE', ]
)
app.add_url_rule(
    '/adv/',
    view_func=AdvertisementView.as_view('advertisements_post'),
    methods=['POST', ]
)
