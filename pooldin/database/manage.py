from sqlalchemy import create_engine
from flask.ext.script import prompt_bool
from . import db as current_db


class DBCompiler(object):
    def __init__(self, db=None, semicolon=True, separator='\n\n'):
        if db is None:
            db = current_db

        self.semicolon = semicolon
        self.separator = separator
        self.db = db
        self.queue = []

    @property
    def engine(self):
        if not hasattr(self, '_engine'):
            url = '%s://' % self.db.engine.url.drivername
            self._engine = create_engine(url,
                                         strategy='mock',
                                         executor=self.dump)
        return self._engine

    def dump(self, sql, *multiparams, **params):
        statement = '%s' % sql.compile(dialect=self.engine.dialect)
        statement = statement.strip()

        if self.semicolon:
            statement = statement.rstrip(';')
            statement = '%s;' % statement.strip()

        self.queue.append(statement)

    def clear(self):
        self.queue = []

    def compile(self, sql=None, separator=None):
        if separator is None:
            separator = self.separator

        if sql:
            self.clear()
            self.dump(sql)

        statement = separator.join(self.queue)
        self.clear()
        return statement

    def drop_all(self, separator=None):
        self.clear()
        self.db.metadata.drop_all(self.engine, checkfirst=False)
        return self.compile(separator=separator)

    def create_all(self, separator=None):
        self.clear()
        self.db.metadata.create_all(self.engine, checkfirst=False)
        return self.compile(separator=separator)


class DBManager(object):

    def __init__(self, db=None):
        if db is None:
            db = current_db

        self.db = db
        self.apps = []
        self.compiler = DBCompiler(db=self.db)

    def add_app(self, app):
        if app in self.apps:
            return

        self.db.init_app(app)
        self.apps.append(app)
        return self

    def remove_app(self, app):
        if app and app in self.apps:
            self.apps.remove(app)

    def create_all(self):
        for app in self.apps:
            with app.app_context():
                self.db.create_all(app=app)
        self.create_fixtures()

    def create_fixtures(self):
        pass

    def drop_all(self, prompt=None):
        message = prompt

        if message is None:
            message = "Are you sure you want to lose all your data"

        if message and not prompt_bool(message):
            return False

        for app in self.apps:
            with app.app_context():
                self.db.drop_all(app=app)

        return True

    def reset_all(self):
        if self.drop_all():
            self.create_all()

    def print_all(self):
        self.print_drop_all()
        print ''
        self.print_create_all()

    def print_drop_all(self):
        print self.compiler.drop_all(separator='\n')

    def print_create_all(self):
        print self.compiler.create_all()
