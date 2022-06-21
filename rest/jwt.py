from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from db.models import User


def jwt_admin_required(func):
    def inner1(*args, **kwargs):
        verify_jwt_in_request()
        user = User.query.get(email=get_jwt_identity())
        if not user.is_admin:
            return {'msg': 'only for admins'}, 401
        returned_value = func(*args, **kwargs)
        return returned_value
    return inner1
