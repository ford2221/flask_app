from my_app import db

from flask_wtf  import  FlaskForm 
from wtforms  import  StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, EqualTo
from flask_login import  current_user 
from flask_user import UserMixin
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash
from flask_admin.contrib.sqla import ModelView

import enum

class RolUser(enum.Enum):
    regular = "regular"
    admin = "admin"


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(300))
    rol = db.Column(Enum(RolUser))
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(255), nullable = False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    # Relationships
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def is_authenticated(sefl):
        return True
    
    @property
    def is_active(sefl):
        return True
    
    @property
    def is_anonymous(sefl):
        return False
    
    def get_id(self):
        return str(self.id)
   
    # def __init__(self, username, pwhash, rol = RolUser.regular):
    #     self.username = username
    #     self.pwhash = generate_password_hash(pwhash)
    #     self.rol = rol
    
    def __repr__(self):
        return '<User %r>' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

class AdminModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return '<h1>Usuario no login</h1>'


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class UserModelView(AdminModelView):

    

    can_edit = True
    create_modal = True
    edit_modal = True
    column_exclude_list = ['pwhash']

    can_export = True
    column_searchable_list = ['username', 'rol']
    comlumn_filters = ['rol']

    '''form_choices = {
    'username': [
        ('MR', 'Mr'),
        ('MRS', 'Mrs'),
        ('MS', 'Ms'),
        ('DR', 'Dr'),
        ('PROF', 'Prof.')
    ]'''

    form_args = {
        'username': {
            'label': 'Usuario',
            'validators': [InputRequired()]
        },
        'pwhash': {
            'label': 'Contraseña',
            'validators': [InputRequired()]
        }
    }

    def on_model_change(self, form, model, is_created):
        print(is_created)
        model.pwhash = generate_password_hash(model.pwhash)

    def edit_form(self, obj=None):
        form = super(UserModelView, self).edit_form(obj)
        form.pwhash.data = ""

        #para borrar un campo
        #del form.pwhash

        return form



class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])
    next = HiddenField('Next')

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired(), EqualTo('confirm')])
    confirm  = PasswordField('Repetir la contraseña')

class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

