# ecommerce Python

##Execução do projeto
<br>criar venv: py -3 -m venv venv<br/>
<br>ativar: venv\Scripts\activate<br/>
<br>instalar dependencias: pip freeze > requirements.txt<br/>



```Python
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

```

<br>Classes do Flask Form. Responsaveis pelos inputs do template de produtos, checkut e cadastros<br/>




```Python
def create_app() -> Flask:
    app = Flask(__name__)
    app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_PHOTOS_DEST
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = SECRET_KEY
    
    db.init_app(app)
    
    with app.app_context():

        from .routes.routes import ecommerce_bp
       
        app.register_blueprint(ecommerce_bp)
     
    return app

```

<br>Factory - Responsavel por fazer a chamada das funções. É Altamente recomendado trabalhar com o Flask nesse formato, pois assim evita erros de importação circular<br/>




```Python

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if Usuarios.id_usuario is None:
            return redirect(url_for('login.login_usuario', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@login.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login.login_usuario'))
    else:
        return redirect(url_for('login.login_usuario'))


```

<br>Funções de ordem superior, "responsveis por faze checagem dos acessos de usuarios<br/>





<br>Projeto ainda esta em desenvolvimento<br/>