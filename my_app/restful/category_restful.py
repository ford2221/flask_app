from flask import request
from flask_restful import Resource, abort, reqparse, marshal_with, fields
from flask_httpauth import HTTPBasicAuth

from my_app.product.model.category import Category

from my_app import db

resource_fields = {
    "name": fields.String
}

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == "admin":
        return True
    return False

class Base:
    def category_to_json(self, category):
        return {
            "id":category.id,
            "name": category.name
        }
    
    def abort_if_doesnt_exist(self, id, json=True):
        category = Category.query.get(id)
        if category is None:
            abort(404, message="categoría {} no exite".format(id))

        if(json):
            return self.category_to_json(category)

        return category

class CategoryRestFul(Resource, Base):

    @auth.login_required
    @marshal_with(resource_fields, envelope="Categoria")
    def get(self, id):
        return self.abort_if_doesnt_exist(id, False)

    def patch(self, id):

        #if not "name" in request.form:
        #    abort(400, message="no se encuentra el campo name")

        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Este campo es requerido")
        args=parser.parse_args()

        c = self.abort_if_doesnt_exist(id, False)
        c.name= args['name'] #request.form

        db.session.add(c)
        db.session.commit()

        return self.abort_if_doesnt_exist(c.id)
    
    def delete(self, id):

        c = self.abort_if_doesnt_exist(id, False)
 
        db.session.delete(c)
        db.session.commit()

        return {"msg":"dale pues"}

    
class CategoryRestFulList(Resource, Base):

    def get(self):
        categories = Category.query.all()
        res=[]
        for c in categories:
            res.append(self.category_to_json(c))
        return res

    def post(self):

        if not "name" in request.form:
            abort(400, message="no se encuentra el campo name")

        c = Category(request.form['name'])
        db.session.add(c)
        db.session.commit()

        return self.abort_if_doesnt_exist(c.id)

class CategoryRestFulListFilter(Resource, Base):

    @marshal_with(resource_fields, envelope="Categoria")
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("filter", required=True, help="Especifica la búsqueda")
        args=parser.parse_args()

        filter = args['filter']

        categories = Category.query.filter(Category.name.like('%{0}%'.format(filter))).all()

        return categories