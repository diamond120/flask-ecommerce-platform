from __future__ import absolute_import

from app.extensions.database import db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import func

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import current_app
from sqlalchemy import Table, MetaData, Float, Integer,ForeignKey,DateTime, Boolean, String, Column
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, composite, mapper, relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method




class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {"schema": "loja"}
    cod_usuario = column_property(db.Column(db.Integer, primary_key=True))
    nomeusuario =db.Column(db.String)
    cod_endereco = db.Column(db.Integer)
    email = db.Column(db.String)
    password = db.Column(db.String)
    datalogado = db.Column(db.DateTime)
    data_cadastro = db.Column(db.DateTime)
    status = db.Column(db.String)
    data_atualizado = db.Column(db.DateTime)
    #order = db.relationship('OrderItem', back_populates='usuarios')
 

    def __repr__(self):
        return f"<nomeusuario={self.nomeusuario}, nomeusuario={self.nomeusuario}>"
    

class Produtos(db.Model):
    __tablename__ = 'Produtos'
    __table_args__ = {"schema": "loja"}
    cod_produto = column_property(db.Column(db.Integer, primary_key=True))
    sku = db.Column(db.String,nullable=True)
    nome_produto = db.Column(db.String,nullable=True)
    quantidade = db.Column(db.Integer)
    custo = db.Column(db.Float)
    valor = db.Column(db.Float)
    desconto =db.Column(db.Float)
    venda = db.Column(db.Float)
    estoque = db.Column(db.Integer)
    descricao = db.Column(db.String)
    data_atualizacao = db.Column(db.Date)
    marca = db.Column(db.String,nullable=True)
    imagem = db.Column(db.String,nullable=True)
    atributos = db.Column(db.String,nullable=True)
    orders = db.Column(db.Integer)


class Pedidos(db.Model):
      
    __tablename__ = 'Pedidos'
    __table_args__ = {"schema": "loja"}
    cod_pedido = column_property(db.Column(db.Integer, primary_key=True))
    referencia = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    cod_produto = column_property(db.Column(db.Integer))
    valor = db.Column(db.Float)
    desconto = db.Column(db.Float)
    margem = db.Column(db.Float)
    cod_endereco = db.Column(db.Integer)
    cod_cliente = db.Column(db.Integer)
    data_atualizacao = db.Column(db.DateTime)
    datacriacao = db.Column(db.String)
    statuspedido = db.Column(db.String)
    #items = db.relationship('OrderItem', backref='cod_pedido', lazy=True)

    @hybrid_property
    def order_total(self):
        return db.session.query(
            db.func.sum(OrderItem.quantidade * Produtos.preco)).join(
            Produtos).filter(OrderItem.cod_pedido == self.cod_pedido).scalar() + 1000
    def quantity_total(self):

        return db.session.query(
            db.func.sum(OrderItem.quantidade)).filter(OrderItem.cod_pedido == self.cod_pedido).scalar()
    

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    __table_args__ = {"schema": "loja"}
    cod_orderitem = db.Column(db.Integer, primary_key=True)

    cod_pedido = column_property(db.Column(db.Integer, ForeignKey('Pedidos.cod_pedido')))
    cod_usuario =  column_property(db.Column(db.Integer, ForeignKey('usuarios.cod_usuario')))
    cod_produto = column_property(db.Column(db.Integer, ForeignKey('Produtos.cod_produto')))
    datacadastro = db.Column(db.DateTime)
    quantidade = db.Column(db.Integer,nullable=True)

    def __repr__(self):

        return f"<cod_orderitem={self.cod_orderitem}, nomeusuario={self.cod_orderitem}>"

