from app import db


class User(db.Model):  # type: ignore
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

# class video(db.Document): TODO
#     name = db.StringField(required=True)
#     email = db.StringField(required=True, unique=True)
#     password = db.StringField(required=True)
#     role = db.StringField(required=True, default='admin')  # TODO: CHANGE IT!

#     @property
#     def is_admin(self):
#         return self.role == 'admin'
