from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, MetaData, Float, Integer,ForeignKey,DateTime, Boolean, String, Column
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.automap import automap_base


db = SQLAlchemy()
def configure_product(app):
    db.init_app(app)
    app.db = db





Product = db.Table(
"Product",
db.metadata,
Column('id',Integer,primary_key=True),
Column('nome',String),
Column('preco',Float),
Column('saldo',Float),
Column('descricao',String),
Column('marca',String),
Column('imagem',String),
Column('orders', Integer,ForeignKey("Order.id"), nullable=False),
schema="dbo",extend_existing=True)


Order = db.Table(
"Order",
db.metadata,
Column('id',Integer,primary_key=True),
Column('referencia',String),
Column('nome',Float),
Column('sobrenome',Float),
Column('telefone',String),
Column('email',String),
Column('endereco',String),
Column('cidade',String),
Column('estado',String),
Column('pais',String),
Column('status',String),
Column('pagamento',String),
Column('orders',back_populates="Product"),
schema="dbo",extend_existing=True)


def order_total(self):
        return db.session.query(db.func.sum(Order_Item.quantidade * Product.preco)).join(Product).filter(Order_Item.order_id == self.id).scalar() + 1000

def quantity_total(self):
        return db.session.query(db.func.sum(Order_Item.quantidade)).filter(Order_Item.order_id == self.id).scalar()



Order_Item = db.Table(
"Order_Item",
db.metadata,
Column('id',Integer,primary_key=True),
Column('order_id',Integer,ForeignKey('order.id')),
Column('product_id',Integer,ForeignKey('product.id')),
Column('quantidade',Integer),
schema="dbo",extend_existing=True)

