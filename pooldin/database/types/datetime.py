import pytz

from sqlalchemy.types import TypeDecorator, DATETIME


class DateTimeTZ(TypeDecorator):
    impl = DATETIME

    def __init__(self, timezone=pytz.UTC):
        super(DateTimeTZ, self).__init__()
        self.timezone = timezone

    def process_bind_param(self, value, dialect):
        if value.tzinfo is None:
            value = self.timezone.localize(value)
        elif value.tzname() != self.timezone.zone:
            value = value.astimezone(self.timezone)
        return value

    def process_result_value(self, value, dialect):
        value = self.timezone.localize(value)
        return value
