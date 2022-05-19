from flask.views import MethodView
from flask import request
from werkzeug import abort
from my_app.product.model.product import Product
from my_app.rest_api.helper.request import sendResJson
from my_app import app, db

import json

class ProductApi(MethodView):

    #Obtener la lista de todos los products
    def get(self, id=None):
        products = Product.query.all()
        print (products)

        if id:
            product = Product.query.get(id)
            res = productToJson(product)
        else:
            res = []
            for p in products:
                res.append(productToJson(p))
        return sendResJson(res, None, 200)

# Esta function es para registrar products
    def post(self):
        if not request.form:
            return sendResJson(None, 'no parameters', 403)


        #validaciones del campo name
        if not 'name' in request.form:
            return sendResJson(None, 'no parameters name', 403)
        
        if len(request.form['name']) < 3:

            return sendResJson(None, 'name invalido', 403)


        #validaciones del campo de precio

        if not 'price' in request.form:
            return sendResJson(None, 'no parameters price', 403)
        
        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None, 'precio invalido', 403)
        
        #if request.form['price'] is not float:
            #return 'precio invalido',403
        
         #validaciones categoria_id

        if not 'category_id' in request.form:
            return 'no parameters categoria',403
        
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None, 'categoria_id invalido', 403)

        p = Product(request.form['name'], request.form['price'], request.form['category_id'])
        db.session.add(p)
        db.session.commit()
        return sendResJson(productToJson(p),None,200)
        
#function para actualizar products
    def put(self,id):
        p = Product.query.get(id)

        if not p:
            return sendResJson(None, 'producto  no existe', 403)

        if not 'category_id' in request.form:
            return 'no parameters categoria',403
        
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None, 'categoria_id invalido', 403)
        
        p.name = request.form['name']
        p.price = request.form['price']
        p.category_id = request.form['category_id']

        db.session.add(p)
        db.session.commit()
        return sendResJson( 'producto actualizado', None, 200)

#function para eliminar un producto
    def delete(self, id):
        product = Product.query.get(id)

        if not product:
            return sendResJson(None, 'producto  no existe', 403)

        db.session.delete(product)
        db.session.commit()
        return sendResJson( 'producto eliminado', None, 200)

'''
esta function nos facilita obtener los atributos de la tabla Product en 
 un diccionario
'''
def productToJson(product: Product):
   return  {
                "id": product.id,
                "name": product.name,
                "category_id": product.category.id,
                "category": product.category.name
            }

''' 
Es la authenticación en postman
'''

api_username='admin'
api_password= '12345'

def protect(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if api_username == auth.username and api_password == auth.password:
            return f(*args, **kwargs)
        #print(auth)
        return abort(401)
    return decorated


#product_view = ProductApi.as_view('product_view')
product_view = protect(ProductApi.as_view('product_view'))

''' 
Ahi termina la authenticación en postman
'''

app.add_url_rule('/api/product/', view_func=product_view, methods=['GET', 'POST'])

app.add_url_rule('/api/product/<int:id>', view_func=product_view, 
methods=['GET', 'DELETE', 'PUT'])
