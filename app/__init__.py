#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask

from config import SQLALCHEMY_DATABASE_URI




db = SQLAlchemy()
def create_app() -> Flask:
    app = Flask(__name__)
    #app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_PHOTOS_DEST
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['DEBUG'] = True
    #app.config['SECRET_KEY'] = SECRET_KEY
    
#https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

    db.init_app(app)
   #configure(app)
    with app.app_context():
        from .routes.routes import ecommerce_bp
        db.create_all()
       
        app.register_blueprint(ecommerce_bp)

    return app