from flask import Flask,Blueprint
from router.main import  main_bl
from router.auth import  auth_bl
from extensions import db , bcrypt , login_manager
from models import Todo , Task , User_table, User_base , Student
from flask_bcrypt import Bcrypt


def create_app(config_file  = "settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User_base.query.get(int(user_id))

    app.register_blueprint(main_bl)
    app.register_blueprint(auth_bl)
    app.run(debug=True)
    return app

