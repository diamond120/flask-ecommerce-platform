from importlib import import_module

from dynaconf import FlaskDynaconf

def load_extensions(app):
    
    for extension in app.config.EXTENSIONS:
        print(extension)
        # extensão path factory
        module_name, factory = extension.split(":")
        # Dynamically import extension module.
        #Importação dinamica de modulos
        ext = import_module(module_name)
        # Call factory
        getattr(ext, factory)(app)


def init_app(app, **config):
    FlaskDynaconf(app, **config)