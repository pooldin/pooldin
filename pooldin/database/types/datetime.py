import pytz

from sqlalchemy.types import TypeDecorator, DateTime


class DateTimeTZ(TypeDecorator):
    impl = DateTime

    def __init__(self, tzinfo=pytz.UTC, *args, **kwargs):
        super(DateTimeTZ, self).__init__(*args, **kwargs)
        self.tz = tzinfo

    def process_bind_param(self, value, dialect):
        if value.tzinfo is None:
            value = self.tz.localize(value)
        elif value.tzname() != self.tz.zone:
            value = value.astimezone(self.tmz)
        return value

    def process_result_value(self, value, dialect):
        value = self.tz.localize(value)
        return value
