from flask import Blueprint
from . import auth, main

Routes = Blueprint('routes', __name__,
				   template_folder='templates')

Routes.add_url_rule('/', 'main', view_func=main.main)
Routes.add_url_rule('/logout', 'logout', view_func=auth.logout)
Routes.add_url_rule('/login', 'login', view_func=auth.login,
					methods=['POST', 'GET'])

