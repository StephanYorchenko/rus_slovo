from flask import Flask, session
from flask_login import LoginManager, current_user

from api import Config
from model import DBUser
from routes import Routes
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'routes.login'
login.login_message = 'Подалуйста, войдите, чтобы посмотреть эт страницу'


@login.user_loader
def load_user(id):
    user = DBUser.get_user(id=int(id))
    session['role'] = user.role
    session['name'] = user.name
    print(session['name'])
    return user

bootsrap = Bootstrap(app)

app.register_blueprint(Routes)
app.secret_key = 'sfadghkjlkdljhfl2t471'

if __name__ == '__main__':
    app.run()
