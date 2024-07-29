from flask import Flask
from __init__ import login_manager
from routes import main_bp
from auth import auth_bp

def sub_app():
    app = Flask(__name__)
    app.secret_key = '36c33b4e9b8892d52cca70841865626b0546eb0e8dc0967edb43662d0c39ddb6'
    app.config['SECRET_KEY'] = '36c33b4e9b8892d52cca70841865626b0546eb0e8dc0967edb43662d0c39ddb6'

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
