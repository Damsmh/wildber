from .models import User, Product, session

def UserInBase(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all()

def GetId(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all()