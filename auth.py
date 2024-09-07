from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import RegistrationForm, LoginForm, UpdateLoginForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect("/sora_login")


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        hashed_confirm_password = generate_password_hash(form.confirm_password.data)
        User.create(username=form.username.data, password_hash=hashed_password, confirm_password_hash=hashed_confirm_password)
        flash('あなたのアカウントが作成されました！ログインできるようになりました!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('others_templates/user_register.html', form=form)

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

@auth_bp.route('/edit_login', methods=['GET', 'POST'])
@login_required
def edit_login():
    form = UpdateLoginForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            if form.new_password.data == form.confirm_new_password.data:
                current_user.password_hash = generate_password_hash(form.new_password.data)
                current_user.username = form.username.data
                current_user.save()
                flash('Your login information has been updated successfully!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('New passwords do not match.', 'danger')
        else:
            flash('Current password is incorrect.', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('others_templates/edit_user.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトできました！', 'success')
    return redirect(url_for('auth.login'))
