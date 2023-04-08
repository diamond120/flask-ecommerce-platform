from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import current_app

from datetime import datetime
from sqlalchemy import func


db = SQLAlchemy()
def configure_product(app):
    db.init_app(app)
    app.db = db



photos = UploadSet('photos', IMAGES)
configure_uploads(current_app, photos)

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


class Product(db.Model):
    __tablename__ = 'Produtos'
    __table_args__ = {"schema": "loja"}
    cod_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String,nullable=True)
    preco = db.Column(db.Float,nullable=True)
    saldo = db.Column(db.Integer,nullable=True)
    descricao = db.Column(db.String,nullable=True)
    marca = db.Column(db.String,nullable=True)
    imagem = db.Column(db.String,nullable=True)
    
    orders = db.relationship('OrderItem', backref='cod_produto', lazy=True)
 


class AddProduct(FlaskForm):
    name = StringField('Nome')
    price = IntegerField('preco')
    stock = IntegerField('saldo')
    description = TextAreaField('descricao')
    image = FileField('imagem', validators=[FileAllowed(IMAGES, 'Nao encontrado.')])


class AddToCart(FlaskForm):
    quantidade = IntegerField('Quantidade')
    id = HiddenField('ID')



class OrderItem(db.Model):
     __tablename__ = 'order_item'
     __table_args__ = {"schema": "loja"}
     cod_orderitem = db.Column(db.Integer, primary_key=True,nullable=False)
     cod_pedido =   db.relationship('Order',back_populates="items")
     produtos =  db.relationship('Product', back_populates="orders")

     datacadastro = db.Column(db.DateTime)
     quantidade = db.Column(db.Integer,nullable=True)

class Order(db.Model):
      
      __tablename__ = 'Pedidos'
      __table_args__ = {"schema": "loja"}
      cod_pedido = db.Column(db.Integer, primary_key=True)
      referencia = db.Column(db.String)
      quantidade = db.Column(db.Integer)
      cod_produto = db.Column(db.Integer)
      valor = db.Column(db.Float)
      desconto = db.Column(db.Float)
      margem = db.Column(db.Float)
      cod_endereco = db.Column(db.Integer)
      cod_cliente = db.Column(db.Integer)
      data_atualizacao = db.Column(db.DateTime)
      datacriacao = db.Column(db.String)
      statuspedido = db.Column(db.String)
      items = db.relationship('OrderItem', backref='order', lazy=True)

      def order_total(self):
        return db.session.query(db.func.sum(OrderItem.quantidade * Product.preco)).join(Product).filter(OrderItem.cod_orderitem == self.cod_pedido).scalar() + 1000

    
      def quantity_total(self):

        return db.session.query(db.func.sum(OrderItem.quantidade)).filter(OrderItem.cod_orderitem == self.cod_pedido).scalar()


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {"schema": "loja"}
    cod_usuario = db.Column(db.Integer, primary_key=True)
    nomeusuario =db.Column(db.String)
    cod_endereco = db.Column(db.Integer)
    email =db.Column(db.String)
    password = db.Column(db.String)
    datalogado = db.Column(db.DateTime)
    data_cadastro =db.Column(db.DateTime)
    status = db.Column(db.String)

