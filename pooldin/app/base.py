import os

from werkzeug.wsgi import SharedDataMiddleware

from flask import Flask
from flask.ext.assets import Environment

from .. import path
from ..database import db

from . import settings
from .config import EnvMixin
from .restrict import RestrictMiddleware
from .rules import RulesMixin
from .session import ItsdangerousSessionInterface
from .setup import InitMixin


class BaseApp(Flask, RulesMixin, EnvMixin, InitMixin):

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
