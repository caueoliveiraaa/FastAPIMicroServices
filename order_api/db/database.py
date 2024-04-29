from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import sqlalchemy.orm
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    inspect,
    Float,
    create_engine
)


Base = sqlalchemy.orm.declarative_base()


class OrderDb(Base):
    __tablename__ = "Order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    item_description = Column(String, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    item_price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    
    def __repr__(self):
        return f'{self.item_description}_{self.id}'


def get_db_session(db_url: str) -> sessionmaker:
    db_engine = create_engine(db_url, echo=False)
    if not database_exists(db_url):
        create_database(db_url)
        
    inspector = inspect(db_engine)
    if not inspector.has_table(OrderDb.__tablename__):
        Base.metadata.create_all(db_engine)
        
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
