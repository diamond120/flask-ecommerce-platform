
from flask import  make_response, jsonify, Response, abort
from flask import render_template


def register_handlers(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Error Handlers')
        return

    @app.errorhandler(403)
    def forbidden_page(*args, **kwargs):
     
        return render_template("handlers.html"), 403

    @app.errorhandler(404)
    def page_not_found(*args, **kwargs):
        return render_template("handlers.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(*args, **kwargs):
       
        return render_template("handlers.html"), 405

    @app.errorhandler(500)
    def server_error_page(*args, **kwargs):
        
        return render_template("handlers.html"), 500
