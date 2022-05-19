from flask import Blueprint, session, render_template, request, url_for, redirect, flash, get_flashed_messages

from my_app.auth.model.user import User, LoginForm, RegisterForm
from my_app import db

auth = Blueprint('auth',__name__)


@auth.route('/register',  methods = ( 'GET' ,  'POST' ))
def register():
    form = RegisterForm()#meta={'csrf':False}

    if form.validate_on_submit ():
        if User.query.filter_by(username=form.username.data).first():
            flash('El usuario ya se encuentra registrado', 'danger')
        else:
            p = User(form.username.data, form.password.data)
            #p = Product(request.form.get['name'], request.form.get['price'])
            db.session.add(p)
            db.session.commit()
            flash('Usuario creado con éxito...!')
            return redirect(url_for('fauth.register'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/register.html', form = form, title = 'register')


@auth.route('/login',  methods = ( 'GET' ,  'POST' ))
def login():
    form = LoginForm()#meta={'csrf':False}

    if form.validate_on_submit ():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            #registerar session
            session['username']= user.username
            session['rol']= user.rol.value
            session['id']= user.id
            flash('Bienvenido de nuevo' +user.username)
            return redirect(url_for('product.index'))
        else:
           flash('Usuario o contraseñas incorrectos', 'danger')
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/login.html', form = form, title = 'login')

@auth.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username')
    session.pop('rol')
    session.pop('id')
    return redirect(url_for('auth.login'))