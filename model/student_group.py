from api import db_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String

from api import db_session

Base = declarative_base()


class DBClass(Base):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    @staticmethod
    def get_class(**kwargs):
        s = db_session()
        class_ = s.query(DBClass).filter_by(**kwargs).first()
        s.close()
        return class_
