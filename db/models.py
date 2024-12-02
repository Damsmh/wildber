from sqlalchemy import ForeignKey, Column, ForeignKeyConstraint, create_engine
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Session
from config_data.config import Config, load_config

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String())
    user_id = Column(Integer, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, user_id={self.user_id!r})"

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, unique=True)
    brand = Column(String())
    name = Column(String())
    reviewRating = Column(Float)
    feedbacks = Column(Integer)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"
    
class Favourite(Base):
    __tablename__ = "favorites_product"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    

    def __repr__(self) -> str:
        return f"Favorite(id={self.id!r})"
    
config: Config = load_config()
engine = create_engine(config.db_engine.url)
Base.metadata.create_all(bind=engine)
session = Session(engine)





