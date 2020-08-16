import os


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'university2035'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
							  or 'postgresql://postgres:123@localhost/main'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

