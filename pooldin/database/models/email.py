from .. import db
from ..common import DisabledMixin, BaseModel


class Email(DisabledMixin, BaseModel):

    __table_args__ = (
        db.UniqueConstraint("user_id", "primary"),
    )

    user = db.relationship('User', backref='emails', lazy='dynamic')
    user_id = db.Column(db.BigInteger(unsigned=True),
                        db.ForeignKey('user.id'),
                        nullable=False)

    primary = db.Column(db.Boolean, default=False, nullable=False)
    address = db.Column(db.String(254),
                        unique=True,
                        nullable=False,
                        index=True)

    def __init__(self, **kw):
        super(Email, self).__init__(**kw)
        self.update_field('user', kw.get('user'))
        self.update_field('address', kw.get('address'))
        self.update_field('primary', kw.get('primary'))

    def __repr__(self):
        return '<Email %r>' % self.address
