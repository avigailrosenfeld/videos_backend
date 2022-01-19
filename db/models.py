from . import db


class User(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    role = db.StringField(required=True, default='admin')  # TODO: CHANGE IT!

    @property
    def is_admin(self):
        return self.role == 'admin'
