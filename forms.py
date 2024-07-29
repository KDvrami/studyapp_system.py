from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("この項目は入力が必須です")])
    password = PasswordField('Password', validators=[DataRequired("この項目は入力が必須です")])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("この項目は入力が必須です")])
    password = PasswordField('Password', validators=[DataRequired("この項目は入力が必須です")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.get_or_none(username=username.data)
        if user:
            raise ValidationError('違うユーザー名を使用してください。')
