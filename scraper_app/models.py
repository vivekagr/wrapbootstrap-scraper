from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
import settings


DeclarativeBase = declarative_base()


def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(settings.DATABASE)


class Template(DeclarativeBase):
    """ Template model """
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    item_hash = Column('item_hash', String)
    title = Column('title', String)
    thumbnail = Column('thumbnail', String, nullable=True)
    description = Column('description', Text, nullable=True)
    creator = Column('creator', String, nullable=True)
    when = Column('when', String)
    bootstrap_version = Column('bootstrap_version', String, nullable=True)
    cost_single = Column('cost_single', Integer)
    cost_multiple = Column('cost_multiple', Integer, nullable=True)
    cost_extended = Column('cost_extended', Integer, nullable=True)
    purchases = Column('purchases', Integer)
