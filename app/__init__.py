from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_moment import Moment
# TODO: (milestone 3) import LoginManager and Moment extensions here
login = LoginManager()
login.login_view = 'auth.login'
db = SQLAlchemy()
moment = Moment()
# TODO: (milestone 3) create LoginManager object and configure the login view as 'auth.login', i.e, `login` route in `auth` Blueprint. 
# TODO: (milestone 3) create Moment object

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER 
    app.template_folder = config_class.TEMPLATE_FOLDER
    moment.init_app(app)
    db.init_app(app)
    login.init_app(app)
    # TODO: (milestone 3) Configure the app object for login using `init_app` function. 
    # TODO: (milestone 3) Configure the app object for moment using `init_app` function. 

    # blueprint registration
    from app.Controller.errors import bp_errors as errors
    app.register_blueprint(errors)
    from app.Controller.auth_routes import bp_auth as auth
    app.register_blueprint(auth)
    from app.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)

    if not app.debug and not app.testing:
        pass
        # ... no changes to logging setup

    return app
