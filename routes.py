from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/home")
@login_required
def home():
    return "Welcome to the home page!"
