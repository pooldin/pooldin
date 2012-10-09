import os
from functools import wraps

from flask.ext.script import Manager, Server, prompt, prompt_pass
from flask.ext.assets import ManageAssets

from pooldin import create_app
from pooldin.database import db
from pooldin.database.manage import DBManager
#from pooldin.database.models import User, Email
from pooldin.app.convert import to_int

manager = Manager(create_app)
manager.app = manager.create_app()
manager.add_command("assets", ManageAssets(manager.app.assets))

# Modify debug server to lisen on 0.0.0.0
port = os.environ.get('PORT')
port = to_int(port) or 5000
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

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


#@manager.command
#@handle_interrupts
#def adduser():
#    address = prompt('Email', default=None)
#    if not address:
#        return
#
#    addressExists = Email.query.filter_by(address=address).first()
#    if addressExists:
#        print 'Email already exists.'
#        return
#
#    username = prompt('Username', default=None)
#    if not username:
#        return
#
#    usernameExists = User.query.filter_by(username=username).first()
#    if usernameExists:
#        print 'Username already exists.'
#        return
#
#    password = prompt_pass('Password', default=None)
#    if not password:
#        return
#
#    password_confirm = prompt_pass('Confirm Password', default=None)
#    if password != password_confirm:
#        print 'Passwords do not match.'
#        return
#
#    user = User()
#    user.enabled = True
#    user.username = username
#    user.password = password
#
#    db.session.add(user)
#    db.session.commit()
#
#    email = Email()
#    email.address = address
#    email.primary = True
#    email.user_id = user.id
#
#    db.session.add(email)
#    db.session.commit()


@manager.command
def loadfixtures():
    db_manager.create_fixtures()


if __name__ == "__main__":
    manager.run()
