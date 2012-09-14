from .. import db


class NameMixin(object):
    name = db.Column(db.String(255), nullable=False)


class NullNameMixin(object):
    name = db.Column(db.String(255))


class DescriptionMixin(object):
    description = db.Column(db.Text)
