from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/sora_login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        try:
            user = User.get(User.username == username)
            if user.password == password:
                login_user(user, remember=remember)
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password')
        except User.DoesNotExist:
            flash('Invalid username or password')

    return render_template('sora_login.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
