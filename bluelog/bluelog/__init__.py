from bluelog.settings import config
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.extensions import bootstrap, mail, db, ckeditor, moment, debugtoolbar, login_manager, csrf, migrate
import os
from flask import Flask, render_template
from bluelog.commands import register_commands
from bluelog.models import Admin, Category, Comment
from flask_wtf.csrf import CSRFError
from flask_login import current_user


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_errors(app)
    register_commands(app)
    register_logging(app)
    register_shell_context(app)
    register_template_context(app)
    register_commands(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    debugtoolbar.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app)


def register_blueprint(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin,
                    categories=categories,
                    unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def bad_request(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def bad_request(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',
                               description=e.description), 400


def register_command(app):
    pass