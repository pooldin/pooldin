from werkzeug.exceptions import Forbidden


class RestrictMiddleware(object):

    def __init__(self, app, whitelist=None, blacklist=None):
        self.app = app
        self.whitelist = whitelist or []
        self.blacklist = blacklist or []

    def __call__(self, environ, start_response):
        if not self.whitelist and not self.blacklist:
            return self.app(environ, start_response)

        environ = environ or dict()
        ips = environ.get('HTTP_X_FORWARDED_FOR', '').split(',')
        ip = None

        if ips:
            ip = ips[0].strip()

        allowed = self.is_whitelisted(ip)
        allowed = allowed and not self.is_blacklisted(ip)

        if not allowed:
            return Forbidden()(environ, start_response)

        return self.app(environ, start_response)

    def is_whitelisted(self, ip):
        if not self.whitelist:
            return True

        if not ip:
            return False

        return ip in self.whitelist

    def is_blacklisted(self, ip):
        if not self.blacklist:
            return False

        if not ip:
            return False

        return ip in self.blacklist
