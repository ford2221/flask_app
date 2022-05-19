
# Customize the Register form:
from flask_user.forms import RegisterForm,ChangeUsernameForm
from wtforms.validators import DataRequired
from wtforms import ValidationError
from wtforms import validators,  StringField
from my_app.auth.model.user import User

class CustomRegisterForm(RegisterForm):
    # Add a country field to the Register form
    country = StringField('Country', validators=[DataRequired()])

class CustomChangeUsernameForm(ChangeUsernameForm):
    new_username = StringField('Nuevo Usuario', validators =[
        validators.DataRequired('Usuario es requerido')

    ])
    
    def validate_new_username(form, field):
        user = User.query.filter_by(username=field.data).first()

        if user:
            raise ValidationError('Este usuario ya es en uso, por favor intente otro usuario')