#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask

from config import SQLALCHEMY_DATABASE_URI,SECRET_KEY,UPLOADED_PHOTOS_DEST



db = SQLAlchemy()

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