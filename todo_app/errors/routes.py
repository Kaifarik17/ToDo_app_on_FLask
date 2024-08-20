from flask import render_template, redirect, url_for

from todo_app.errors import errors_bp


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
