from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla

from werkzeug.security import generate_password_hash



from app.models import Produtos,Usuarios
from app.extensions.database import db

admin = Admin()


class UserAdmin(sqla.ModelView):
    column_list = ['username']
    can_edit = False

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)


def init_app(app):
    
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(sqla.ModelView(Produtos, db.session))
    admin.add_view(UserAdmin(Usuarios, db.session))