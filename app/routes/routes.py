import random
from flask import session, redirect, render_template, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from typing import TypeVar
from collections.abc import Iterable

from flask import current_app,Blueprint
from werkzeug.utils import secure_filename
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from sqlalchemy import select
from ..models.models import Product, Order,OrderItem
from ..controllers.forms import AddToCart,AddProduct, Checkout, photos,configure_uploads
from dotenv import load_dotenv

from urllib.parse import urlparse

load_dotenv()


S = TypeVar('S')
Response = Iterable[S] | int

db = SQLAlchemy()
def configure(app):
    db.init_app(app)
    app.db = db


ecommerce_bp = Blueprint("ecommerce", __name__)

current_app.config['UPLOADED_PHOTOS_DEST'] = os.getenv('IMAGENS')


from typing import TypeVar, List

T = TypeVar('T')

def handle_cart() -> T:
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

        products.append({'id' : product.id, 'nome' : product.nome, 'preco' : product.preco, 'imagem' : product.imagem, 'quantidade' : quantidade, 'total': total,'index': index})
        index += 1
    
    grand_total_plus_shipping = grand_total + 1000

    return products, grand_total, grand_total_plus_shipping, quantity_total


@ecommerce_bp.route('/')
def index() -> str:
    #products = Product.query.all()
    #, products=products
    return render_template('index.html')

@ecommerce_bp.route('/product/<id>')
def product(id) -> str:
    product = Product.query.filter_by(id=id).first()

    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)


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
        try:
            order = Order()
            form.populate_obj(order)
            order.reference = ''.join([random.choice('ABCDE') for _ in range(5)])
            order.status = 'PENDING'

            for product in products:
                order_item = OrderItem(quantity=product['quantidade'], product_id=product['id'])
                order.items.append(order_item)

                product = Product.query.filter_by(id=product['id']).update({'saldo' : Product.saldo - product['quantidade']})

            db.session.add(order)
            db.session.commit()

            session['cart'] = []
            session.modified = True
        except:
            pass
        return redirect(url_for('ecommerce.index'))

    return render_template('checkout.html', form=form, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)

@ecommerce_bp.route('/admin/')
def admin() -> str:
    try:
        products = Product.query.all()
    except:
        pass
    try:
        products_in_stock = Product.query.filter(Product.saldo > 0).count()

        orders = Order.query.all()

        return render_template('admin/index.html'
                            , admin=True, products=products, products_in_stock=products_in_stock, orders=orders)

    except:
        return "Notfound"

@ecommerce_bp.route('/admin/add', methods=['GET', 'POST'])
def add() -> (Response | str):
    form = AddProduct()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))
        print(form.name.data)
        print(form.price.data)
        print(form.stock.data)
        print(form.description.data)
        print(form.image.data)

        new_product = Product(name=form.name.data, 
                              price=form.price.data, stock=form.stock.data, 
                              description=form.description.data, image=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('ecommerce.admin'))

    return render_template('admin/add-product.html', admin=True, form=form)


@ecommerce_bp.route('/admin/order/<order_id>')
def order(order_id: int) -> str:
    order = Order.query.filter_by(id=int(order_id)).first()

    return render_template('admin/view-order.html', order=order, admin=True)
