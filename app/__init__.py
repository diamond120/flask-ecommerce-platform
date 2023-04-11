from flask import Flask

from app.extensions import configuration
from .config import SQLALCHEMY_DATABASE_URI,SECRET_KEY
from .handlers import register_handlers



def minimal_app(**config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 370
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = SECRET_KEY

    configuration.init_app(app, **config)
    register_handlers(app)
    return app



def create_app(**config):
    app = minimal_app(**config)
    configuration.load_extensions(app)
    register_handlers(app)
    return app




