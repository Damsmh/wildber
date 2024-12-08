from .models import User, Product, Favourite, session

def UserInBase(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all()

def UserCount():
    return session.query(User).count()

def UserList():
    return session.query(User.username, User.user_id).all()

def AddUser(username: str, user_id: int):
    session.add(User(username=username, user_id=user_id))
    session.commit()

def UserBan(username: str):
    session.query(User).filter(User.username == username).update({'is_banned': True}) 
    session.commit()

def UserUnban(username: str):
    session.query(User).filter(User.username == username).update({'is_banned': False}) 
    session.commit()

def addPrime(username: str):
    session.query(User).filter(User.username == username).update({'is_prime': True}) 
    session.commit()

def UserProductsCount(user_id: int):
    return session.query(Favourite).filter(Favourite.user_id == user_id).count()

def removePrime(username: str):
    session.query(User).filter(User.username == username).update({'is_prime': False}) 
    session.commit()

def DeleteUser(user_id: int):
    user = session.query(User).filter(User.user_id == user_id).one()
    session.delete(user)
    session.commit()

def GetId(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all()

def ProductInBase(product_id: int):
    return session.query(Product.id).filter(Product.product_id == product_id).all()

def AddProduct(product: dict):
    session.add(Product(
        product_id=product['id'],
        brand=product['brand'],
        name=product['name'],
        reviewRating=product['reviewRating'],
        feedbacks=product['feedbacks'],
        link=product['link'],
        price=product['price'],
    ))
    session.commit()

def AddFavourite(user_id: int, product_id: int):
    session.add(Favourite(
        user_id=user_id,
        product_id=product_id,
    ))
    session.commit()

def DeleteFavourite(user_id: int, product_id: int):
    fav = session.query(Favourite).filter(Favourite.user_id == user_id, Favourite.product_id == product_id).one()
    session.delete(fav)
    session.commit()

def ProductInFavourite(user_id: int, product_id: int):
    return session.query(Favourite.id).filter(Favourite.product_id == product_id, Favourite.user_id == user_id).all()