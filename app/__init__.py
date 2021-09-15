from flask import Flask
from flask_login import LoginManager
from config import Config
app = Flask(__name__)
# the config attribute of the flask object loads the configuration values from the Config module
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = 'info'
login_manager.login_message = "You can not access this page, please login"

from app import routes