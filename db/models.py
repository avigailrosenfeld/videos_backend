from . import db
from flask_restful import Resource, Api


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # name = db.StringField(required=True)
    # email = db.StringField(required=True, unique=True)
    # password = db.StringField(required=True)
    # role = db.StringField(required=True, default='admin')  # TODO: CHANGE IT!

    # @property
    # def is_admin(self):
    #     return self.role == 'admin'
    def __repr__(self):
        return '<User %r>' % self.username


class Index(Resource):
    def get(self):
        ret = []
        res = User.query.all()
        for user in res:
            ret.append(
                {
                    'username': user.username,
                    'email': user.email
                }
            )
        return ret, 200

# class video(db.Document):
#     name = db.StringField(required=True)
#     email = db.StringField(required=True, unique=True)
#     password = db.StringField(required=True)
#     role = db.StringField(required=True, default='admin')  # TODO: CHANGE IT!

#     @property
#     def is_admin(self):
#         return self.role == 'admin'
