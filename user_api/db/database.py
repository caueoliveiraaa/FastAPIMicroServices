from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sqlalchemy.orm
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    inspect,
    create_engine
)


Base = sqlalchemy.orm.declarative_base()


class UserDb(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    
    
    def __repr__(self):
        return f'{self.full_name}_{self.id}'


def get_db_session(db_url: str) -> sessionmaker:
    db_engine = create_engine(db_url, echo=False)
    if not database_exists(db_url):
        create_database(db_url)
    
    inspector = inspect(db_engine)
    if not inspector.has_table(UserDb.__tablename__):
        Base.metadata.create_all(db_engine)
    
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
