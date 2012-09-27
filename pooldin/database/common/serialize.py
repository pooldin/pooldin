import calendar
from datetime import datetime
import json

from flask import current_app


class JSONSerializationMixin(object):

    def to_json(self, model_dict=None, fields=None):
        model_dict = model_dict or self.to_dict(fields=fields)
        for (field, value) in model_dict.items():
            if isinstance(value, datetime):
                model_dict[field] = int(calendar.timegm(value.timetuple()))
            if isinstance(value, bool):
                model_dict[field] = 'true' if value else 'false'
        return json.dumps(model_dict)
