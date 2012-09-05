from functools import wraps

from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from pooldin import create_app
from pooldin.database.manage import DBManager


manager = Manager(create_app)
manager.app = manager.create_app()
manager.add_command("assets", ManageAssets(manager.app.assets))

db_manager = DBManager()
db_manager.add_app(manager.app)


def handle_interrupts(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        try:
            return fn(*args, **kw)
        except KeyboardInterrupt:
            return
        except EOFError:
            print ''
            return
    return wrapper


@manager.shell
def shell_context():
    from pooldin.database import models
    db_manager.db.app = manager.app
    return dict(app=manager.app,
                db=db_manager.db,
                db_manager=db_manager,
                models=models)


@manager.command
def createdb():
    db_manager.create_all()


@manager.command
@handle_interrupts
def dropdb():
    db_manager.drop_all()


@manager.command
@handle_interrupts
def resetdb():
    db_manager.reset_all()


@manager.command
def printdb():
    db_manager.print_all()


@manager.command
def printdropdb():
    db_manager.print_drop_all()


@manager.command
def printcreatedb():
    db_manager.print_create_all()


if __name__ == "__main__":
    manager.run()
