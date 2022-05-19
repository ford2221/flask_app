from my_app import db

from decimal import Decimal

from  flask_wtf  import  FlaskForm 
from  wtforms  import  StringField, DecimalField, SelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, NumberRange

class Product(db.Model):
    __tablename__ = 'products'


    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    file = db.Column(db.String(255))
    #category  = db.relationship('Category', backref='products', lazy='select')
    

    def __init__(self, name, price, category_id, file):
        self.name = name
        self.price = price
        self.category_id = category_id
        self.file = file
    
    def __repr__(self):
        return '<Product %r>' % (self.name)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name ,
            'price': self.price,

        }

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    price = DecimalField('Precio', validators=[InputRequired(), NumberRange(min=Decimal('0.0'))])
    category_id = SelectField('Categoria', coerce=int)
    file = FileField('archivo') #, validators=[FileRequired()]
