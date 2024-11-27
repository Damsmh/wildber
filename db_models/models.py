from sqlalchemy import ForeignKey, Column, create_engine
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Session
from config_data.config import Config, load_config

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    product = Column(ForeignKey("product.id"))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey("user.id"))
    brand = Column(String())
    name = Column(String())
    reviewRating = Column(Float)
    feedbacks = Column(Integer)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"
    

config: Config = load_config()
engine = create_engine(config.db_engine.url)
Base.metadata.create_all(bind=engine)
session = Session(engine)





