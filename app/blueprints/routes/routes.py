from flask import Blueprint, jsonify
from flask import render_template
from flask import session, redirect, url_for
import random


from app.extensions.database import db
ecommerce_bp = Blueprint("ecommerce", __name__)
from app.models import Produtos,Pedidos,OrderItem
from app.controllers.controllers import AddProduct,AddToCart,Checkout




def handle_cart():
    lista_Produtos = []
    grand_total = 0
    index = 0
    quantity_total = 0

    for item in session['cart']:
        produto = Produtos.query.filter_by(cod_produto=item['cod_produto']).first()
       
        quantidade = int(item['quantidade'])
        total = quantidade * produto.valor
        
        grand_total += total

        quantity_total += quantidade

        lista_Produtos.append({'cod_produto' : produto.cod_produto,
                          'nome' : produto.nome, 'valor' :  produto.valor,
                            'imagem' : produto.imagem, 'quantidade' : quantidade, 'total': total, 'index': index})
        index += 1
        print(lista_Produtos)
    grand_total_plus_shipping = grand_total + 1000

    return produto, grand_total, grand_total_plus_shipping, quantity_total


@ecommerce_bp.route('/')
def index():
    products = Produtos.query.limit(4).all()
    
    print(products)
    return render_template('index.html', products=products)


@ecommerce_bp.route('/product/<cod_produto>')
def product(cod_produto):
    product = Produtos.query.filter_by(cod_produto=cod_produto).first()

    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)

@ecommerce_bp.route('/quick-add/<cod_produto>')
def quick_add(cod_produto):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'cod_produto' : cod_produto, 'quantidade' : 1})
    session.modified = True

    return redirect(url_for('ecommerce.index'))

@ecommerce_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():

        session['cart'].append({'cod_produto' : form.cod_produto.data, 'quantidade' : form.quantidade.data})
        session.modified = True

    return redirect(url_for('ecommerce.index'))

@ecommerce_bp.route('/cart')
def cart():
    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

    return render_template('cart.html', products=products, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)


@ecommerce_bp.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))


@ecommerce_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = Checkout()

    products, grand_total, grand_total_plus_shipping, quantity_total = handle_cart()

    if form.validate_on_submit():

        order = Pedidos()
        form.populate_obj(order)
        Pedidos.cod_pedido = ''.join([random.choice('ABCDE') for _ in range(5)])
        Pedidos.statuspedido = 'PENDING'

        for product in products:
            order_item = OrderItem(quantity=product['quantidade'], product_id=product['cod_produto'])
            order.items.append(order_item)

            product = Produtos.query.filter_by(cod_produto=product['cod_produto']).update({'quantidade' : Produtos.quantidade - product['quantidade']})

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True

        return redirect(url_for('index'))

    return render_template('checkout.html', form=form, grand_total=grand_total, grand_total_plus_shipping=grand_total_plus_shipping, quantity_total=quantity_total)

@ecommerce_bp.route('/admin')
def admin():
    products = Produtos.query.all()
    products_in_stock = Produtos.query.filter(Produtos.quantidade > 0).count()

    orders = Pedidos.query.all()

    return render_template('admin/index.html', admin=True, products=products, products_in_stock=products_in_stock, orders=orders)
'''
@ecommerce_bp.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.imagem.data))

        new_product = Product(name=form.name.data, price=form.valor.data, stock=form.quantidade.data, descricao=form.descricao.data, imagem=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)
'''
@ecommerce_bp.route('/admin/order/<cod_pedido>')
def order(cod_pedido):
    order = Pedidos.query.filter_by(id=int(cod_pedido)).first()

    return render_template('admin/view-order.html', order=order, admin=True)



def init_app(app):
    
    app.register_blueprint(ecommerce_bp)

 
 
