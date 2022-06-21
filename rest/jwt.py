from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from db.dal_mysql.dal_users import DalUsers


def jwt_admin_required(func):
    def inner1(*args, **kwargs):
        verify_jwt_in_request()
        user = DalUsers.get_user_by_email(get_jwt_identity())
        if not user.is_admin:
            return {'msg': 'only for admins'}, 401
        returned_value = func(*args, **kwargs)
        return returned_value
    return inner1
