from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters."),
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class QuestionForm(FlaskForm):
    question= TextAreaField('Question', validators=[DataRequired(), Length(max=255)])
    option_a = StringField('Option A', validators=[DataRequired(), Length(max=100)])
    option_b = StringField('Option B', validators=[DataRequired(), Length(max=100)])
    option_c = StringField('Option C', validators=[DataRequired(), Length(max=100)])
    option_d = StringField('Option D', validators=[DataRequired(), Length(max=100)])
    correct_option = SelectField('Correct Option', choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')
    ], validators=[DataRequired()])
    submit = SubmitField('Next')

class QuizForm(FlaskForm):
    selected_option = RadioField('Answer', choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Answer')