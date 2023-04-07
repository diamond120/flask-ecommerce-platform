
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import current_app


photos = UploadSet('photos', IMAGES)

configure_uploads(current_app, photos)

class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('price')
    stock = IntegerField('stock')
    description = TextAreaField('description')
    image = FileField('image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])

class AddToCart(FlaskForm):
    quantidade = IntegerField('Quantidade')
    id = HiddenField('ID')

class Checkout(FlaskForm):
    nome = StringField('Nome')
    sobrenome = StringField('Sobrenome')
    Telefone = StringField('Numero')
    email = StringField('Email')
    Endereco = StringField('Endereco')
    cidade = StringField('Cidade')
    estado = SelectField('Estado', choices=[('SP', 'Campinas'), ('SP', 'São Bernardo'), ('SP', 'Ribeirao Preto')])
    pais = SelectField('Pais', choices=[('SP', 'São Jose Dos Campos'), ('BA', 'Salvador'), ('MG', 'Belo Horizonte')])
    payment_type = SelectField('Payment Type', choices=[('CK', 'Check'), ('WT', 'Wire Transfer')])
