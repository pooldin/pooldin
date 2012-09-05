from datetime import datetime

from flask import request

from .. import db


def remote_ip():
    if not request:
        return

    ips = request.headers.getlist("X-Forwarded-For")

    if len(ips) > 0:
        return ips[0]

    if hasattr(request, 'remote_addr') and request.remote_addr:
        return request.remote_addr


class TrackTimeMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime,
                         default=datetime.utcnow,
                         onupdate=datetime.utcnow)


class TrackIPMixin(object):
    # For reasoning around the column length, consult stackoverflow.com:
    #   /questions/1076714/max-length-for-client-ip-address
    remote_ip = db.Column(db.String(45), default=remote_ip, onupdate=remote_ip)
