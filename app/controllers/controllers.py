from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES


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


class AddProduct(FlaskForm):
    nome = StringField('Nome')
    preco = IntegerField('preco')
    saldo = IntegerField('saldo')
    descricao = TextAreaField('descricao')
    imagem = FileField('image', validators=[FileAllowed(IMAGES, 'Nao encontrado.')])


class AddToCart(FlaskForm):
    quantidade = IntegerField('quantidade')
    cod_produto = HiddenField('cod_produto')