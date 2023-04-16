from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    usernameOrEmail = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username/Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Login", "class": "text-white"})

class RegisterForm(FlaskForm):
    username = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "text-black"})
    email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    confirmPassword = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Register", "class": "text-white"})

class CreateServerForm(FlaskForm):
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.4','1.19.4')], validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Create"})

class OpPlayerForm(FlaskForm):
    player = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit = SubmitField('submit', render_kw={"value": "Op player"})

class DeopPlayerForm(FlaskForm):
    player = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit = SubmitField('submit', render_kw={"value": "Deop player"})

class WhitelistPlayerForm(FlaskForm):
    player = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit = SubmitField('submit', render_kw={"value": "Whitelist player"})

class UnwhitelistPlayerForm(FlaskForm):
    player = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit = SubmitField('submit', render_kw={"value": "Unwhitelist player"})