from app import db
from db.models import User

# from flask_restful import Resource


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False,
                     default='admin')  # TODO: CHANGE IT!

    @property
    def is_admin(self):
        return self.role == 'admin'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    # def __repr__(self):
    #     return '<User %r>' % self.username


# class Index(Resource):
#     def get(self):
#         ret = []
#         res = User.query.all()
#         for user in res:
#             ret.append(
#                 {
#                     'username': user.username,
#                     'email': user.email
#                 }
#             )
#         return ret, 200

# class video(db.Document):
#     name = db.StringField(required=True)
#     email = db.StringField(required=True, unique=True)
#     password = db.StringField(required=True)
#     role = db.StringField(required=True, default='admin')  # TODO: CHANGE IT!

#     @property
#     def is_admin(self):
#         return self.role == 'admin'
