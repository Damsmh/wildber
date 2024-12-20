from sqlalchemy import ForeignKey, Column, ForeignKeyConstraint, create_engine
from sqlalchemy import String, Integer, Float, BigInteger, Boolean, insert, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from config_data.config import Config, load_config

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    product_id = Column(BigInteger, unique=True)
    preview = Column(String)
    brand = Column(String)
    name = Column(String)
    reviewRating = Column(Float)
    link = Column(String)
    feedbacks = Column(Integer)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"
    
class Favourite(Base):
    __tablename__ = "favorites_product"
    id = Column(Integer, primary_key=True)
    product_id = Column(BigInteger, ForeignKey('product.product_id'))
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    

    def __repr__(self) -> str:
        return f"Favorite(id={self.id!r})"
    
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(BigInteger, unique=True)
    is_prime = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    favourite = relationship(Favourite, cascade='all, delete', backref = "children")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, user_id={self.user_id!r})"
    
class Prices(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(BigInteger)
    price = Column(Integer)
    timestamp = Column(TIMESTAMP)

    def __repr__(self) -> str:
        return f"Prices(id={self.id!r}, product_id={self.product_id!r}, price={self.price!r}, timestamp={self.timestamp!r})"
    
config: Config = load_config()
engine = create_engine(config.db_engine.url)
Base.metadata.create_all(bind=engine)
session = Session(engine)





