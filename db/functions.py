from .models import User, Product, Favourite, Prices, session
from sqlalchemy import select, insert
from datetime import datetime

async def UserInBase(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all() != []

async def isBanned(TG: int):
    return session.query(User.id).filter(User.user_id == TG, User.is_banned == True).all() != []

async def UserCount():
    return session.query(User).count()

async def UserList():
    return session.query(User.username, User.user_id).all()

async def AddUser(username: str, user_id: int):
    session.add(User(username=username, user_id=user_id))
    session.commit()

async def UserBan(username: str):
    session.query(User).filter(User.username == username).update({'is_banned': True}) 
    session.commit()

async def UserUnban(username: str):
    session.query(User).filter(User.username == username).update({'is_banned': False}) 
    session.commit()

async def addPrime(username: str):
    session.query(User).filter(User.username == username).update({'is_prime': True}) 
    session.commit()

async def isPrime(uid: str):
    return session.query(User).filter(User.user_id == uid, User.is_prime == True).all() != []

async def UserProductsCount(user_id: int):
    return session.query(Favourite).filter(Favourite.user_id == user_id).count()

async def removePrime(username: str):
    session.query(User).filter(User.username == username).update({'is_prime': False}) 
    session.commit()

async def DeleteUser(user_id: int):
    user = session.query(User).filter(User.user_id == user_id).one()
    session.delete(user)
    session.commit()

async def GetId(TG: int):
    return session.query(User.id).filter(User.user_id == TG).all()

async def ProductInBase(product_id: int):
    return session.query(Product.id).filter(Product.product_id == product_id).all()

async def AddProduct(product: dict):
    session.add(Product(
        product_id=product['id'],
        preview=product['preview'],
        brand=product['brand'],
        name=product['name'],
        reviewRating=product['reviewRating'],
        feedbacks=product['feedbacks'],
        link=product['link'],
        price=product['price'],
    ))
    session.commit()

async def AddFavourite(user_id: int, product_id: int):
    session.add(Favourite(
        user_id=user_id,
        product_id=product_id,
    ))
    session.commit()

async def DeleteFavourite(user_id: int, product_id: int):
    fav = session.query(Favourite).filter(Favourite.user_id == user_id, Favourite.product_id == product_id).one()
    session.delete(fav)
    session.commit()

def ProductInFavourite(user_id: int, product_id: int):
    return session.query(Favourite.id).filter(Favourite.product_id == product_id, Favourite.user_id == user_id).all()

def FavouriteList(user_id: int):
    subquery = select(Favourite.product_id).where(Favourite.user_id == user_id).subquery()
    query = select(Product).where(Product.product_id.in_(select(subquery.c.product_id)))
    result = session.execute(query)
    return result.scalars().all()

def FavouriteUser():
    users = session.execute(select(Favourite.user_id)).all()
    result = {}
    for user in users:
        result[user[0]] = FavouriteList(user[0])
    return result

async def UpdateProductPrice(product_id: int, price: int):
    session.query(Product).filter(Product.product_id == product_id).update({'price': price}) 
    session.commit()

async def FavouriteCount(user_id: int):
    return session.query(Favourite.id).filter(Favourite.user_id == user_id).count()

async def update_price_history(article, current_price):
    query = insert(Prices).values(
        product_id=article,
        price=current_price,
        timestamp=datetime.now()
    )
    await session.execute(query)
    await session.commit()
def get_price_history(article):
    query = (
        session.query(Prices)
        .filter(Prices.product_id == article)
        .order_by(Prices.timestamp.asc())
    )
    return session.execute(query).scalars().all()