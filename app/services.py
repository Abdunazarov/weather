from .models import User
from . import db

def create_user(username, balance):
    new_user = User(username=username, balance=balance)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user_balance(user_id, balance_change):
    user = get_user_by_id(user_id)
    if user and (user.balance + balance_change) >= 0:
        user.balance += balance_change
        db.session.commit()
        return user
    return None

def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
