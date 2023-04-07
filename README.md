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

