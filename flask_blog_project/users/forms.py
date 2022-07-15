from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


from flask_blog_project.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(),
                                                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(
            username=username.data).first()  # здесь username - это поле формы, а username.data - его содержимое
        if user:
            raise ValidationError(
                'This username is occupied, please select another'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email is occupied, please select another'
            )


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remind password')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    picture = FileField('Profiles photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Renew')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is occupied, please select another')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This mail is occupied, please select another')


class RequestResetForm(FlaskForm):
    """Отправка запроса на изменение пароля."""
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Change password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email, you can register it')


class ResetPasswordForm(FlaskForm):
    """ввод нового пароля и подтверждение его изменения"""
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm the password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Set password')

