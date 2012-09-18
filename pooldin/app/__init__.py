import os

from webassets.loaders import YAMLLoader
from flask import request, url_for
from flask.ext.login import current_user

from .. import path, views
from .base import BaseApp


class App(BaseApp):

    name = __name__
    prefix = 'POOLDIN'

    views = views.all

    def init_middleware(self):
        self.before_request(self.restrict_login)
        self.after_request(self.inject_response_headers)

    def restrict_login(self):
        if current_user.is_authenticated():
            return

        login_path = url_for(self.login.login_view)
        if request.path.startswith(login_path):
            return

        return self.login.unauthorized()

    def inject_response_headers(self, resp):
        # Add headers to both force latest IE rendering engine or Chrome Frame.
        resp.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'

        return resp

    def init_extensions(self):
        super(App, self).init_extensions()

        manifest = os.path.join(path, 'assets', 'manifest.yaml')
        bundles = YAMLLoader(manifest).load_bundles()

        for name, bundle in bundles.iteritems():
            self.assets.register(name, bundle)

    def init_processors(self):
        self.context_processor(self.user_context)

    def user_context(self):
        try:
            primary_email = [e.address for e in current_user.emails if e.primary][0]
        except (IndexError, AttributeError):
            primary_email = None
        return dict(user=current_user, primary_email=primary_email)
