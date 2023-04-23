from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    Login form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    usernameOrEmail = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username/Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Login", "class": "text-white"})

class RegisterForm(FlaskForm):
    """
    Register form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    username = StringField('usernameOrEmail', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "text-black"})
    email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "text-black"})
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Password", "type": "password", "class": "text-black"})
    confirmPassword = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Confirm password", "type": "password", "class": "text-black"})
    submit = SubmitField('submit', render_kw={"value": "Register", "class": "text-white"})

class CreateServerForm(FlaskForm):
    """
    Create server form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    serverName = StringField('serverName', validators=[DataRequired()])
    serverVersion = SelectField('serverVersion', choices=[('1.8.8', '1.8.8'), ('1.9.4', '1.9.4'), ('1.10.2', '1.10.2'), ('1.11.2', '1.11.2'), ('1.12.2', '1.12.2'), ('1.13.2', '1.13.2'), ('1.14.4', '1.14.4'), ('1.15.2', '1.15.2'), ('1.16.5', '1.16.5'), ('1.17.1', '1.17.1'), ('1.18.2', '1.18.2'), ('1.19.4','1.19.4')], validators=[DataRequired()])
    submit = SubmitField('submit', render_kw={"value": "Create"})

class OpPlayerForm(FlaskForm):
    """
    Op player form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    player1 = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit1 = SubmitField('submit', render_kw={"value": "Op player"})

class DeopPlayerForm(FlaskForm):
    """
    Deop player form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    player = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit = SubmitField('submit', render_kw={"value": "Deop player"})

class WhitelistPlayerForm(FlaskForm):
    """
    Whitelist player form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    player2 = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit2 = SubmitField('submit', render_kw={"value": "Whitelist player"})

class UnwhitelistPlayerForm(FlaskForm):
    """
    Unwhitelist player form

    Args:
        FlaskForm (FlaskForm): The flask form
    """
    player2 = StringField('player', validators=[DataRequired()], render_kw={"placeholder": "Minecraft player name"})
    submit2 = SubmitField('submit', render_kw={"value": "Unwhitelist player"})