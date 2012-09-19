from sqlalchemy.ext.hybrid import hybrid_property

from werkzeug.security import generate_password_hash, check_password_hash

from flask.ext import login

from .. import db
from ..common import BaseModel, IDMixin, NullNameMixin, DisabledMixin


class User(BaseModel, IDMixin, NullNameMixin, DisabledMixin, login.UserMixin):

    username = db.Column(db.String(40), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    @hybrid_property
    def display_name(self):
        return self.name or self.username

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self.update_field('username', kw.get('username'))

        password = kw.get('password')

        if password is not None:
            self.password = password

    def is_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.enabled

    @property
    def primary_email(self):
        try:
            email = [e.address for e in self.emails][0]
        except IndexError:
            email = None
        return email


class AnonymousUser(login.AnonymousUser):
    name = 'Anonymous'
