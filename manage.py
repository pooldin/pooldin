import os
from functools import wraps
import json

from flask.ext.script import Manager, prompt, prompt_pass
from flask.ext.assets import ManageAssets

from pooldin import create_app, path
from pooldin.database import db
from pooldin.database.manage import DBManager
from pooldin.database.models import User, Email


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
    loadfixtures()


@manager.command
@handle_interrupts
def dropdb():
    db_manager.drop_all()


@manager.command
@handle_interrupts
def resetdb():
    db_manager.reset_all()
    loadfixtures()


@manager.command
def printdb():
    db_manager.print_all()


@manager.command
def printdropdb():
    db_manager.print_drop_all()


@manager.command
def printcreatedb():
    db_manager.print_create_all()


@manager.command
@handle_interrupts
def adduser():
    address = prompt('Email', default=None)
    if not address:
        return

    addressExists = Email.query.filter_by(address=address).first()
    if addressExists:
        print 'Email already exists.'
        return

    username = prompt('Username', default=None)
    if not username:
        return

    usernameExists = User.query.filter_by(username=username).first()
    if usernameExists:
        print 'Username already exists.'
        return

    password = prompt_pass('Password', default=None)
    if not password:
        return

    password_confirm = prompt_pass('Confirm Password', default=None)
    if password != password_confirm:
        print 'Passwords do not match.'
        return

    user = User()
    user.enabled = True
    user.username = username
    user.password = password

    db.session.add(user)
    db.session.commit()

    email = Email()
    email.address = address
    email.primary = True
    email.user_id = user.id

    db.session.add(email)
    db.session.commit()


@manager.command
def loadfixtures():
    user_fixture_path = os.path.join(os.path.dirname(path),
                                     'fixtures',
                                     'users.json')
    with open(user_fixture_path) as fs:
        users = json.load(fs)

    for (username, u) in users.items():
        user = User()
        user.enabled = True
        user.username = username
        user.password = u['password']
        user.about = u['about']

        db.session.add(user)
        db.session.commit()

        email = Email()
        email.address = u['address']
        email.enabled = True
        email.primary = True
        email.user_id = user.id

        db.session.add(email)
        db.session.commit()


if __name__ == "__main__":
    manager.run()
