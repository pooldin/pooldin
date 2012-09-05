import os
import uuid


class EnvMixin(object):

    ENV = 'dev'
    SECRET_KEY = uuid.uuid4().hex

    name = __name__

    def configure(self):
        self.configure_prefix()
        self.configure_env()
        self.configure_envars()
        self.configure_app()
        self.configure_wsgi()
        return self

    def configure_prefix(self):
        if hasattr(self, 'prefix'):
            self.prefix = self.prefix.rstrip('_')

        if not hasattr(self, 'prefix'):
            self.prefix = self.__class__.__name__.upper()

    def configure_env(self):
        self.env = self.from_env('ENV', type=lambda e: e.lower())

        if hasattr(self, 'settings') and hasattr(self.settings, self.env):
            self.config.from_object(getattr(self.settings, self.env))

    def configure_envars(self):
        pass

    def configure_app(self):
        pass

    def configure_wsgi(self):
        pass

    def from_env(self, key, name=None, default=None, type=None):
        name = name or key
        prefix_name = '_'.join((self.prefix.rstrip('_'), name))

        value = os.environ.get(prefix_name, None) or \
            os.environ.get(name, None) or \
            getattr(self, key, None)

        if value is not None and type is not None:
            try:
                value = type(value)
            except ValueError:
                value = default
        elif value is None:
            value = default

        if value is not None:
            self.config[key] = value
            return value
