#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_login import LoginManager
from config import SQLALCHEMY_DATABASE_URI,SECRET_KEY,UPLOADED_PHOTOS_DEST
from flask import  request, make_response, jsonify,current_app, Response, abort
from flask_migrate import Migrate

import time
def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return


#Handlers
def register_handlers(app):
    if current_app.config.get('DEBUG') is True:
        current_app.logger.debug('Skipping error handlers in Debug mode')
        return

    @current_app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"Error":"not found error"}), 404

    @current_app.errorhandler(500)
    def internal_error(error):
        return jsonify({"Error":"internal error"}), 500

    @current_app.errorhandler(500)
    def ModuleNotFoundError(*args, **kwargs):
        return jsonify({"Error":"Server Error"}), 500

    @current_app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return jsonify({"Error":"EndPoint NotFound"}), 404
   
    @current_app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
  
        return jsonify({"Error":"Method not found"}), 400


db = SQLAlchemy()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['UPLOADED_PHOTOS_DEST'] = UPLOADED_PHOTOS_DEST
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 370
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = SECRET_KEY
    
    '''
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
        ),
        )
    '''

    #celery_app = celery_init_app(app)
    db.init_app(app)
    """
    Essas funções precisam ser passadas dentro da Factory
    """
    '''
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is not None:
            return Usuarios.query.get(int(user_id))
        return None

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Faça o login!')
        return redirect(url_for('login.login_usuario'))
    '''
    
    with app.app_context():

        from .routes.routes import ecommerce_bp
       
        app.register_blueprint(ecommerce_bp)
        register_handlers(current_app)
     
    return app