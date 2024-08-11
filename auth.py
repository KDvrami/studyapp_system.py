from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect("/sora_login")


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        User.create(username=form.username.data, password_hash=hashed_password)
        flash('あなたのアカウントが作成されました！ログインできるようになりました!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('others_templates/register.html', form=form)

@auth_bp.route('/sora_login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('ログイン出来ました！', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('ログインできませんでした。ユーザー名、パスワードを確認してください。', 'danger')
    return render_template('others_templates/sora_login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトできました！', 'success')
    return redirect(url_for('auth.login'))
