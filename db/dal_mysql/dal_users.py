from app import db
from db.models import User


class DalUsers():
    @staticmethod
    def get_user_by_email(email: str) -> User:
        return db.session.query(User).filter(
            User.email == email).first()

    @staticmethod
    def create_user(user: User) -> int:
        user_id = db.session.add(user)
        db.session.commit()
        return user_id

    @staticmethod
    def get_user_by_id(id: str) -> User:
        return db.session.query(User).filter(
            User.id == id).first()
