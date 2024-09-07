from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("この項目は入力が必須です")])
    password = PasswordField('Password', validators=[DataRequired("この項目は入力が必須です")])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired("この項目は入力必須です")])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("この項目は入力が必須です")])
    password = PasswordField('Password', validators=[DataRequired("この項目は入力が必須です")])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired("この項目は入力必須です")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.get_or_none(username=username.data)
        if user:
            raise ValidationError('違うユーザー名を使用してください。')

class UpdateLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Login Info')