from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from website.models import User


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Country', validators=[DataRequired(), Length(min=3, max=75)])
    city = StringField('City', validators=[DataRequired(), Length(min=3, max=85)])
    text = TextAreaField('Few words about yourself', validators=[DataRequired(), Length(max=200)])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError('That username is taken. Please, choose another one.')

    def validate_email(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError('That email is taken. Please, choose another one.')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class EditAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Country', validators=[DataRequired(), Length(min=3, max=75)])
    city = StringField('City', validators=[DataRequired(), Length(min=3, max=85)])
    text = TextAreaField('Few words about yourself', validators=[DataRequired(), Length(max=200)])
    picture = FileField('Profile Picture', validators=[FileAllowed(['png', 'jpg', 'bmp'])])
    submit = SubmitField('Update')

    def edit_username(self, field):
        if username.data != current_user.username:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError('That username is taken. Please, choose another one.')

    def edit_email(self, field):
        if email.data != current_user.email:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                raise ValidationError('That email is taken. Please, choose another one.')


class UserSearchForm(FlaskForm):

    username = StringField('Username', validators=[Length(max=20)])
    country = StringField('Country', validators=[Length(max=75)])
    city = StringField('City', validators=[Length(max=85)])
    submit = SubmitField('Search')
