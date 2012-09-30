from sqlalchemy.ext.declarative import declared_attr

from .. import db, common
from .currency import Currency


class Account(common.Model, common.EnabledMixin):
    """
    For no particular reason, it has been decided that account balances can
    never be larger than 10^100 + 0.9999. To correctly handle a number of this
    magnitude, the NUMERIC/DECIMAL datatype must be used.

    To calculate the precision we start with the significant digits, 100.
    Since our base is 10, we have one more significant digit to account for,
    101. Lastly, since we have to account for 4 decimal places, we have 4 more
    significant digits to add: 105.

    Hence, our total precision is 105 and our scale (decimal places) is 4.

    The following was used to guide the decision process:
    http://en.wikipedia.org/wiki/Orders_of_magnitude_(numbers)
    """
    __abstract__ = True

    @declared_attr
    def currency_id(cls):
        return db.Column(db.BigInteger(unsigned=True),
                         db.ForeignKey('currency.id'),
                         nullable=False)

    balance = db.Column(db.Numeric(precision=105, scale=4),
                        nullable=False,
                        default=0)

    @classmethod
    def filter_by(cls, currency=None, query=None):
        if hasattr(currency, 'id'):
            currency = currency.id

        if not query:
            query = cls.query

        if currency and isinstance(currency, basestring):
            query = query.join(Currency)
            return query.filter(Currency.code == currency)

        if currency:
            return query.filter(cls.currency_id == currency)

        return query

    @classmethod
    def first(cls, *args, **kw):
        return cls.filter_by(*args, **kw).first()


class UserAccount(Account):
    __tablename__ = 'user_account'

    user_id = db.Column(db.BigInteger(unsigned=True),
                        db.ForeignKey('user.id'),
                        nullable=False)

    user = db.relationship('User', backref='accounts', lazy='dynamic')
    currency = db.relationship('Currency', backref='user_accounts')

    @classmethod
    def filter_by(cls, user=None, currency=None):
        if hasattr(user, 'id'):
            user = user.id

        if not user:
            return

        query = cls.query.filter(cls.user_id == user)
        return super(UserAccount, cls).filter_by(currency=currency,
                                                 query=query)


class GroupAccount(Account):
    __tablename__ = 'group_account'

    group_id = db.Column(db.BigInteger(unsigned=True),
                         db.ForeignKey('group.id'),
                         nullable=False)

    group = db.relationship('Group', backref='accounts', lazy='dynamic')
    currency = db.relationship('Currency', backref='group_accounts')

    @classmethod
    def filter_by(cls, group=None, currency=None):
        if hasattr(group, 'id'):
            group = group.id

        if not group:
            return

        query = cls.query.filter(cls.group_id == group)
        return super(GroupAccount, cls).filter_by(currency=currency,
                                                  query=query)
