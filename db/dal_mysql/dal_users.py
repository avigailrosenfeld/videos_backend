from typing import Dict, Union
from app import db
from db.models import User


class DalUsers:
    @staticmethod
    def get_user_by_email(email: str) -> User:
        return db.session.query(User).filter(
            User.email == email).first()

    @staticmethod
    def get_user_by_id(id: str) -> User:
        return db.session.query(User).filter(
            User.id == id).first()

    @staticmethod
    def get_all_users() -> User:
        return db.session.query(User).filter().all()

    @staticmethod
    def create_user(user: User) -> int:
        db.session.add(user)
        db.session.commit()
        return user.id

    @staticmethod
    def update_user(body: Dict, id: str) -> int:  # type: ignore
        user = DalUsers.get_user_by_id(id=id)
        for key, value in body.items():
            setattr(user, key, value)
        db.session.commit()
        return user.id

    @staticmethod
    def delete_user_by_id(id: str) -> None:
        user = DalUsers.get_user_by_id(id=id)
        db.session.delete(user)
        db.session.commit()
