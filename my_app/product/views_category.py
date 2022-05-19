
from flask import Blueprint, render_template, request, url_for, redirect, flash, get_flashed_messages
from werkzeug import abort
from sqlalchemy.sql.expression import not_
from flask_login import login_required

from my_app import db
from my_app import rol_admin_need, mail, app, get_locale
from my_app.product.model.category import Category
from my_app.product.model.category import CategoryForm
from flask_mail import Message
from flask_babel import gettext

from collections import namedtuple

categoryBp = Blueprint('category',__name__)

@categoryBp.before_request
@login_required
@rol_admin_need
def constructor():
   pass


@categoryBp.route('/category')
@categoryBp.route('/category/<int:page>')
def index(page=1):

   name = gettext('name')
   gettext('save')
   gettext('update')
   gettext('create')
   gettext('delete')

   print(name)

   print(get_locale())

   msg = Message('Hola Flask', recipients= ['ford@udemyflask.net'])
   msg.body = 'Hola muchachos'
   msg.html = "<b>testing</b>"

   with app.open_resource("static/uploads/mediaMte.png") as fp:
      msg.attach("logo.png", "image/png", fp.read())

   #mail.send(msg)

   return render_template('category/index.html', categories=Category.query.paginate(page, 5), title = 'category')
   #return render_template('category/index.html', categories=Category.query.filter_by(name='Categoryo1').paginate(page, 5))

@categoryBp.route('/category-create',  methods = ( 'GET' ,  'POST' ))
def create():
   form = CategoryForm()#meta={'csrf':False}
   if form.validate_on_submit ():
      p = Category(request.form['name'])
      #p = Category(request.form.get['name'], request.form.get['price'])
      db.session.add(p)
      db.session.commit()

      flash('Categoria creado con éxito...!')
      return redirect(url_for('category.create'))
   if form.errors:
      flash(form.errors, 'danger')
   return render_template('category/create.html', form = form, title = 'category')


@categoryBp.route('/category-update/<int:id>', methods = ['GET','POST'])
def update(id):
   category = Category.query.get_or_404(id)

   group = namedtuple('Group', ['phoneCode','countryCode','phone'])

   g1 = group('416','+58','7568474')
   g2 = group('414','+63','1234474')
   g3 = group('412','+56','7532474')

   phones = {'phones': [g1, g2, g3]}

   form = CategoryForm(data = phones)#meta={'csrf':False}

   #del form.phoneList

   c = Category(name='Cattee 1')

   if request.method == 'GET':
      form.name.data = category.name
      form.id.data = category.id

   if  form.validate_on_submit ():
      category.name = request.form['name']

      form.populate_obj(c)
      print(c.name)

      db.session.add(category)
      db.session.commit()
      #return 'category  updated'
      flash('Categoria actualizado con éxito...!')
      return redirect(url_for('category.index', id = category.id))
   if form.errors:
      flash(form.errors, 'danger')
   return render_template('category/update.html', category = category, form = form, title = 'category')

@categoryBp.route('/category-delete/<int:id>')
def delete(id):
   p = Category.query.get_or_404(id)
   db.session.delete(p)
   db.session.commit()
   flash('Categoria eliminado con éxito...!')
   return redirect(url_for('category.index'))

@categoryBp.route('/filter/<int:id>')
def filter(id):
   p = Category.query.get(id)
   return render_template('category/filter.html', category=p)


@categoryBp.app_template_filter('iva')
def iva_filter(category):
   if category["price"]:
      return category["price"] * .20 + category["price"]
   return "Sin precio"

#@category.route('/test')
#def test(): 
   #p = Category.query.limit(2).all()
   #p = Category.query.limit(2).first()
    #p = Category.query.order_by(Category.id).all()
   #p = Category.query.order_by(Category.id.desc).all()
   #p = Category.query.get({'id':'Categoryo1'}) answer = NOne,just a prove
   #p = Category.query.filter_by(name = 'Categoryo4').all()
   #p = Category.query.filter(Category.id > 1).all()
   #p = Category.query.filter(Category.id > 1).first()
   #p = Category.query.filter(Category.name.like('P%')).all() busqueda con el nombre que contenga P otras letras
   #p = Category.query.filter(not_(Category.id > 1)).all()
  # print(p)
   #return "Flask"
