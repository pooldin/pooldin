import os

from werkzeug.wsgi import SharedDataMiddleware

from flask import Flask
from flask.ext.assets import Environment
from flask.ext.login import LoginManager
from flask.ext.gravatar import Gravatar

from .. import path
from ..database import db
from ..database.models import User, AnonymousUser

from . import settings
from .config import EnvMixin
from .restrict import RestrictMiddleware
from .rules import RulesMixin
from .session import ItsdangerousSessionInterface
from .setup import InitMixin


class BaseApp(Flask, RulesMixin, EnvMixin, InitMixin):

    login_anonymous = AnonymousUser
    login_view = 'user_login'
    login_refresh_view = 'user_login'
    login_message = 'Please log in to access this page.'

    settings = settings

    def __init__(self, *args, **kw):
        kw['static_folder'] = 'static/media'
        kw['static_url_path'] = '/media'
        super(BaseApp, self).__init__(*args, **kw)
        self.configure()

    def configure_envars(self):
        self.from_env('SECRET_KEY')
        self.from_env('SESSION_SALT')
        self.from_env('SQLALCHEMY_DATABASE_URI', name='DATABASE_URL')
        self.from_env('WHITELIST', type=lambda s: s.split('|'))
        self.from_env('BLACKLIST', type=lambda s: s.split('|'))

    def configure_app(self):
        salt = self.config.get('SESSION_SALT')
        self.session_interface = ItsdangerousSessionInterface(salt=salt)

    def configure_wsgi(self):
        self.configure_wsgi_static()
        self.configure_wsgi_restrict()

    def configure_wsgi_static(self):
        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
            '/': ('pooldin', 'static')
        })

    def configure_wsgi_restrict(self):
        whitelist = self.config.get('WHITELIST')
        blacklist = self.config.get('BLACKLIST')

        if not whitelist and not blacklist:
            return

        self.wsgi_app = RestrictMiddleware(self.wsgi_app,
                                           whitelist=whitelist,
                                           blacklist=blacklist)

    def init_extensions(self):
        db.init_app(self)
        self.assets = Environment(self)
        self.assets.directory = os.path.join(path, 'assets')
        self.assets.url = '/media'

        self.login = LoginManager()
        self.login.anonymous_user = self.login_anonymous
        self.login.login_view = self.login_view
        self.login.login_message = self.login_message
        self.login.refresh_view = self.login_refresh_view
        self.login.init_app(self)
        self.login.user_loader(self.load_user)
        self.login.init_app(self)

        self.gravatar = Gravatar(self,
                                 size=350,  # Default to header profile image size
                                 default='mm',  # Options available at gravatar.com
                                 force_default=False,
                                 force_lower=False)

    def load_user(self, id):
        return User.query.filter_by(id=id).first()
