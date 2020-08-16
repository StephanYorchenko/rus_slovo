from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from . import Config


def db_connect():
	return db.connect



def db_session():
	return db.bdsession



def db_engine():
	return db.engine


class Db(object):
	def __init__(self, test=False):
		self.test = test
		self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
		self.bdsession = sessionmaker(bind=self.engine, autocommit=True)()
		self.connect = self.engine.connect()


db = Db()

