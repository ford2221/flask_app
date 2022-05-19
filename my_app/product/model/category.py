from my_app import db

from  flask_wtf  import  FlaskForm, RecaptchaField
from  wtforms  import  StringField, HiddenField, FormField, FieldList
from wtforms.validators import InputRequired, ValidationError

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category', lazy='select')
    #products = db.relationship('Product', lazy='dynamic', backref=db.backref('category', lazy='select'))
    

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Category %r>' % (self.name)

def check_category2(form, field):
    res = Category.query.filter_by(name = field.data).first()
    if res:
        raise ValidationError('La categoria: %s ya fue tomada' % field.data)

def check_category(contain=True):
    def _check_category(form, field):
        if contain:
            res = Category.query.filter(Category.name.like("%"+field.data+"%")).first()
        else:
            res = Category.query.filter(Category.name.like(field.data)).first()

        if res and form.id.data =="":
            raise ValidationError('La categoria: %s ya fue tomada' % field.data)
        
        if res and form.id.data and res.id != int(form.id.data):
            raise ValidationError('La categoria: %s ya fue tomada' % field.data)
    return _check_category

class PhoneForm(FlaskForm):
    phoneCode = StringField('codigo de telefono')
    countryCode = StringField('codigo pais')
    phone = StringField('telefono')

#class PhoneForm2(FlaskForm):
  #  phoneCode2 = StringField('codigo de telefono2')

class CategoryForm(PhoneForm):#, PhoneForm2
    name = StringField('Nombre', validators=[InputRequired(), check_category(contain=False)])
    id = HiddenField('Id')
    recaptcha = RecaptchaField()
    #phoneList = FormField(PhoneForm)
    #phones = FieldList(FormField(PhoneForm))


