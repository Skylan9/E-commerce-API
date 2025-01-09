from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired
import sqlalchemy as sa
from app import db
from app.models import Users, Status

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(Users).where(
            Users.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class WorkoutForm(FlaskForm):
    name = StringField('Workout plan name', validators=[DataRequired()], render_kw={'autofocus': True})
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('category', validators=[DataRequired()])
    exercises = SelectMultipleField('Exercises', coerce=int)
    status = SelectField("Status", choices=[])
    btn_cancel = SubmitField(label='Cancel',
                         render_kw={'formnovalidate': True})
    submit = SubmitField('Submit')