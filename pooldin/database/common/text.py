from .. import db


class NameMixin(object):
    name = db.Column(db.String(255), nullable=False)


class DescriptionMixin(object):
    description = db.Column(db.Text)
