from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy import (Float, Integer
                        ,ForeignKey,DateTime, Boolean, String, Column)

from datetime import datetime
from sqlalchemy import func


db = SQLAlchemy()
def configure_product(app):
    db.init_app(app)
    app.db = db


class Product(db.Model):
    __tablename__ = 'produtos'
    __bind_key__ = 'BIGDATA'
    __table_args__ = {"schema": "dbo"}
    id = Column(db.Integer, primary_key=True)
    nome = Column(db.String,nullable=True)
    preco = Column(db.Float,nullable=True)
    saldo = Column(db.Integer,nullable=True)
    descricao = Column(db.String,nullable=True)
    marca = Column(db.String,nullable=True)
    imagem = Column(db.String,nullable=True)
    orders = Column(db.Integer,ForeignKey("Order.id"), nullable=False)


class Order(db.Model):
      __tablename__ = 'order'
      __bind_key__ = 'BIGDATA'
      __table_args__ = {"schema": "dbo"}
      id = db.Column(db.Integer, primary_key=True)
      referencia = db.Column(db.String)
      nome = db.Column(db.String)
      sobrenome = db.Column(db.String)
      telefone = db.Column(db.String,nullable=True)
      email = db.Column(db.String,nullable=True)
      endereco = db.Column(db.String,nullable=True)
      cidade = db.Column(db.String,nullable=True)
      estado = db.Column(db.String,nullable=True)
      pais = db.Column(db.String,nullable=True)
      status = db.Column(db.String,nullable=True)
      pagamento = db.Column(db.String,nullable=True)
      orders = db.relationship(db.Integer, back_populates="Product")
      

      def order_total(self):
                return db.session.query(
                     db.func.sum(OrderItem.quantidade * Product.preco)).join(
                     Product).filter(OrderItem.order_id == self.id).scalar() + 1000
      
      def quantity_total(self):
        return db.session.query(
             db.func.sum(OrderItem.quantidade)).filter(OrderItem.order_id == self.id).scalar()


class OrderItem(db.Model):
     __tablename__ = 'order_item'
     __bind_key__ = 'BIGDATA'
     __table_args__ = {"schema": "dbo"}
     id = db.Column(db.Integer, primary_key=True,nullable=False)
     order_id = db.Column(db.Integer,ForeignKey('order.id'),nullable=False)
     product_id = db.Column(db.Integer,ForeignKey('product.id'),nullable=False)
     quantidade = db.Column(db.Integer,nullable=True)

     
