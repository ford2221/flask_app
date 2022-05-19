from flask import Flask, redirect, url_for, request
from  flask_wtf.csrf  import  CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user 
from functools import wraps
# from flask_bootstrap  import  Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_babel import Babel
from flask_user import UserManager
from flask_user.signals import user_registered
from flask_restless import APIManager
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension

#flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os 

app = Flask(__name__)
# Bootstrap(app)


csrf= CSRFProtect(app)

ALLOWED_EXTENTIONS_FILES = (['pdf', 'jpg', 'jpeg','png' , 'gif', 'txt'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/my_app/static/uploads'


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/udemydb'
app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

#flaskrestful
from flask_restful import Api
from my_app.restful.hello_world import HelloWorld
from my_app.restful.category_restful import CategoryRestFul, CategoryRestFulList, CategoryRestFulListFilter

api=Api(app, decorators=[csrf.exempt])
api.add_resource(HelloWorld, '/api/test')
api.add_resource(CategoryRestFul, '/api/category/<int:id>')
api.add_resource(CategoryRestFulList, '/api/category')
api.add_resource(CategoryRestFulListFilter, '/api/category/filter')

from my_app.auth.model.user import Role

#flask admin+++++++++++++++++
from my_app.auth.model.user import User, UserModelView

admin = Admin(app, template_mode ='bootstrap4')
#admin = Admin(app, template_mode ='bootstrap3')
#admin.add_view(UserModelView(User, db.session))

#++++++++++++para el crud 

from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app.auth.model.user import User
# from my_app.product.model.product import Product

# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ModelView(Product, db.session))


######## ++++++++++++fin flask admin


babel = Babel(app)

@babel.localeselector
def get_locale():
    #return 'en'
    return request.accept_languages.best_match(['es', 'en'])

#**************** flask user****************
usermanager = UserManager(app, db, User)


@user_registered.connect_via(app)
def _after_registration_hook(sender, user, **extra):
    rol = Role.query.filter_by(name='Regular').one()
    user.roles.append(rol)
    db.session.add(user)
    db.session.commit()

#**************** flask restless****************
restless_manager = APIManager(app, flask_sqlalchemy_db = db)
restless_manager.create_api(Product, methods = ['POST'])

migrate = Migrate(app, db) #// a descomentar
mail = Mail(app)

#****************** flaks cache
cache = Cache(app)

#+***************** toolbar debug
#toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "user.login" #fauth.login

def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != "admin":
            #login_manager.unauthorized()
            logout_user()
            return redirect(url_for('user.login'))#fauth.login
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper


#+++++++++++++import los controladores
from my_app.invoice.productController import invoiceProductBp
from my_app.product.views_product import productBp
from my_app.product.views_category import categoryBp
from my_app.product.userController import userBp
#from my_app.auth.views import auth
from my_app.fauth.views import fauth
from my_app.spavue.views import spavue

#importar restapi
# from my_app.rest_api.product_api import product_view
# from my_app.rest_api.category_api import category_view

#importart general
import my_app.general.error_handle

# #registrar las vistas
app.register_blueprint(productBp)
app.register_blueprint(categoryBp)
app.register_blueprint(userBp)
app.register_blueprint(invoiceProductBp)
#app.register_blueprint(auth)
app.register_blueprint(fauth)
app.register_blueprint(spavue)

#db.create_all()


@app.template_filter('mydouble')
def mydouble_filter(n:float):
    return n*2
