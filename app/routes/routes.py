from flask import Blueprint, Response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
import random
from flask import session, redirect, render_template, url_for
from ..models.models import Product, Order, Order_Item
import os
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask import current_app
from werkzeug.utils import secure_filename
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from typing import TypeVar, List
from sqlalchemy import select
from models.models import Product, Order,Order_Item



db = SQLAlchemy()
def configure(app):
    db.init_app(app)
    app.db = db


ecommerce_bp = Blueprint("ecommerce", __name__)

current_app.config['UPLOADED_PHOTOS_DEST'] = r'C:\estimadoresteste\ecommerce_flask_app\app\static\imagens'

photos = UploadSet('photos', IMAGES)
configure_uploads(current_app, photos)

class AddProduct(FlaskForm):
    nome = StringField('Nome')
    preco = IntegerField('Preco')
    saldo = IntegerField('Saldo')
    descricao = TextAreaField('Descricao')
    imagem = FileField('Imagem', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])

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


from typing import TypeVar, List

T = TypeVar('T')

def handle_cart() ->T:
    products = list[dict[str,str]]
    grand_total = 0
    index = 0
    quantity_total = 0

    for item in session['cart']:
        product = Product.query.filter_by(id=item['id']).first()

        quantidade = int(item['quantidade'])
        total = quantidade * product.price
        grand_total += total

        quantity_total += quantidade

        products.append({'id' : product.id, 'nome' : product.nome, 'preco' :  product.preco, 'imagem' : product.imagem, 'quantidade' : quantidade, 'total': total, 'index': index})
        index += 1
    
    grand_total_plus_shipping = grand_total + 1000

    return products, grand_total, grand_total_plus_shipping, quantity_total


@ecommerce_bp.route('/')
def index() -> str:
    #products = Product.query.all()
    produto = select([Product])
    result = conn.execute(produto)

    return render_template('index.html', products=products)

@ecommerce_bp.route('/product/<id>')
def product(id) -> str:
    product = Product.query.filter_by(id=id).first()

    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)


'''
@ecommerce_bp.route('/quick-add/<id>')
def quick_add(id: int) -> Response:
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'id' : id, 'quantidade' : 1})
    session.modified = True

    return redirect(url_for('ecommerce.index'))

@ecommerce_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart() -> Response:
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():

        session['cart'].append({'id' : form.id.data, 'quantidade' : form.quantidade.data})
        session.modified = True

    return redirect(url_for('ecommerce.index'))

@ecommerce_bp.route('/cart')
def cart() -> str:
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

    return render_template('cart.html', products=products, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)

@ecommerce_bp.route('/remove-from-cart/<index>')
def remove_from_cart(index: T) -> Response:
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('ecommerce.cart'))

@ecommerce_bp.route('/checkout', methods=['GET', 'POST'])
def checkout() -> (Response | str):
    form = Checkout()

    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

    if form.validate_on_submit():

        order = Order()
        form.populate_obj(order)
        order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
        order.status = 'PENDING'

        for product in products:
            order_item = Order_Item(quantity=product['quantidade'], product_id=product['id'])
            order.items.append(order_item)

            product = Product.query.filter_by(id=product['id']).update({'saldo' : Product.saldo - product['quantidade']})

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True

        return redirect(url_for('ecommerce.index'))

    return render_template('checkout.html', form=form, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)

@ecommerce_bp.route('/admin/')
def admin() -> str:
    products = Product.query.all()
    products_in_stock = Product.query.filter(Product.saldo > 0).count()

    orders = Order.query.all()

    return render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, orders=orders)

@ecommerce_bp.route('/admin/add', methods=['GET', 'POST'])
def add() -> (Response | str):
    form = AddProduct()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))

        new_product = Product(name=form.name.data, price=form.price.data, stock=form.stock.data, description=form.description.data, image=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('ecommerce.admin'))

    return render_template('admin/add-product.html', admin=True, form=form)

@ecommerce_bp.route('/admin/order/<order_id>')
def order(order_id: int) -> str:
    order = Order.query.filter_by(id=int(order_id)).first()

    return render_template('admin/view-order.html', order=order, admin=True)
'''