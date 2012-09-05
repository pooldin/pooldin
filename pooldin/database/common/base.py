from sqlalchemy.ext.declarative import declared_attr

from .. import db

from .active import EnabledMixin
from .identity import IDMixin, UUIDMixin
from .text import NameMixin, DescriptionMixin
from .tracking import TrackTimeMixin, TrackIPMixin
from .update import FieldUpdateMixin


class BaseModel(db.Model,
                IDMixin,
                FieldUpdateMixin,
                TrackTimeMixin,
                TrackIPMixin):

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, **kw):
        self.update_field('enabled', kw.get('enabled'))

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.id)


class BaseConfig(EnabledMixin, NameMixin, DescriptionMixin, BaseModel):
    __abstract__ = True

    def __init__(self, **kw):
        super(BaseConfig, self).__init__(**kw)
        self.update_field('name', kw.get('name'))
        self.update_field('description', kw.get('description'))


class BaseRecord(UUIDMixin, BaseModel):
    __abstract__ = True
