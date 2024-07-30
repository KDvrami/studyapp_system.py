from flask import Flask
from __init__ import login_manager
from routes import main_bp
from auth import auth_bp
from dotenv import load_dotenv
import os

def sub_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
