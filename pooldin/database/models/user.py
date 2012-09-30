from sqlalchemy.ext.hybrid import hybrid_property

from werkzeug.security import generate_password_hash, check_password_hash

from flask.ext import login

from .. import common, db


class User(common.Model,
           common.IDMixin,
           common.NullNameMixin,
           common.DisabledMixin,
           common.SerializationMixin,
           login.UserMixin):

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
        emails = [e.address for e in self.emails if e.primary]
        if not emails:
            return
        return emails[0]

    def to_dict(self, fields=None):
        fields = fields or ['username', 'display_name', 'about', 'created', 'modified', 'enabled']
        return super(User, self).to_dict(fields=fields)


class AnonymousUser(login.AnonymousUser):
    name = 'Anonymous'
