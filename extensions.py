#phần này cài đặt sqlaichemy
from flask_login import login_manager , UserMixin , login_required
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt  = Bcrypt()
login_manager = LoginManager()