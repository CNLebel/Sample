#-*- coding:utf-8 -*-

from flask import Flask,request
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_login import LoginManager, current_user
from flask_gravatar import Gravatar
from flask_babel import Babel,gettext as _

basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()
babel = Babel()
bootstrap = Bootstrap()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



def create_app():
    app = Flask(__name__)
    app.secret_key='hard to guess string'
    # app.config.from_pyfile('babel.cfg')
    app.config['BABEL_DEFAULT_LOCALE']='zh'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    babel.init_app(app)
    Gravatar(app, size=64)


    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    @babel.localeselector
    def get_locale():
        pass

    return app