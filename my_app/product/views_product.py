#from my_app import app
import os
from flask import Blueprint, render_template, request, url_for, redirect, flash, get_flashed_messages
from werkzeug import abort, secure_filename
from sqlalchemy.sql.expression import not_

from flask_login import login_required
from flask_user import roles_required

from my_app import db, app, ALLOWED_EXTENTIONS_FILES
from my_app import rol_admin_need, cache
from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app.product.model.product import ProductForm


productBp = Blueprint('product',__name__)

import time

@productBp.route('/test')
#@cache.cached(timeout= 60)
def test():
   time.sleep(3)
   return 'hola mundo'

@productBp.before_request
@login_required
#@rol_admin_need
@roles_required('Admin')
def constructor():
   pass

def allowed_extentions_file(filename):
   return ('.' in filename and filename.lower().rsplit('.')[1] in ALLOWED_EXTENTIONS_FILES)

@productBp.route('/product')
@productBp.route('/product/<int:page>')
def index(page=1):
   return render_template('product/index.html', products=Product.query.paginate(page, 5), title = 'product')
   #return render_template('product/index.html', products=Product.query.filter_by(name='Producto1').paginate(page, 5))

@productBp.route('/product-create',  methods = ( 'GET' ,  'POST' ))
def create():
   form = ProductForm() #meta={'csrf':False}

   categories = [(c.id, c.name) for c in  Category.query.all()]
   form.category_id.choices = categories

   if form.validate_on_submit ():
      p = Product(request.form['name'], request.form['price'], request.form['category_id'], 
         request.form['file'])
      #p = Product(request.form.get['name'], request.form.get['price'])

      db.session.add(p)
      db.session.commit()

      flash('producto creado con éxito...!')
      return redirect(url_for('product.create'))
   if form.errors:
      flash(form.errors, 'danger')
   return render_template('product/create.html', form = form, title = 'product')


@productBp.route('/product-update/<int:id>', methods = ['GET','POST'])
def update(id):
   product = Product.query.get_or_404(id)
   form = ProductForm()#meta={'csrf':False}

   categories = [(c.id, c.name) for c in  Category.query.all()]
   form.category_id.choices = categories
   
   print(product.category)

   if request.method == 'GET':
      form.name.data = product.name
      form.price.data = product.price
      form.category_id.data = product.category_id


   if  form.validate_on_submit ():
      product.name = request.form['name']
      product.price = request.form['price']
      product.category_id = request.form['category_id']

      file = form.file.data
      if allowed_extentions_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         product.file = filename

      db.session.add(product)
      db.session.commit()
      #return 'product  updated'
      flash('producto actualizado con éxito...!')
      return redirect(url_for('product.index', id = product.id))
   if form.errors:
      print("________")
      flash(form.errors.items(), 'form-error')
   return render_template('product/update.html', product = product, form = form, title = 'product')

@productBp.route('/product-delete/<int:id>')
def delete(id):
   p = Product.query.get_or_404(id)
   db.session.delete(p)
   db.session.commit()
   flash('producto eliminado con éxito...!')
   return redirect(url_for('product.index'))

@productBp.route('/filter/<int:id>')
def filter(id):
   p = Product.query.get(id)
   return render_template('product/filter.html', product=p)


@productBp.app_template_filter('iva')
def iva_filter(product):
   if product["price"]:
      return product["price"] * .20 + product["price"]
   return "Sin precio"

@productBp.route('/show/<int:id>')
def show(id):
   product = Product.query.get_or_404(id)
   return render_template('product/show.html', product=product)

#@product.route('/test')
#def test(): 
   #p = Product.query.limit(2).all()
   #p = Product.query.limit(2).first()
    #p = Product.query.order_by(Product.id).all()
   #p = Product.query.order_by(Product.id.desc).all()
   #p = Product.query.get({'id':'Producto1'}) answer = NOne,just a prove
   #p = Product.query.filter_by(name = 'Producto4').all()
   #p = Product.query.filter(Product.id > 1).all()
   #p = Product.query.filter(Product.id > 1).first()
   #p = Product.query.filter(Product.name.like('P%')).all() busqueda con el nombre que contenga P otras letras
   #p = Product.query.filter(not_(Product.id > 1)).all()
  # print(p)
   #return "Flask"
