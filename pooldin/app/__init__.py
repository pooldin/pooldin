import os

from webassets.loaders import YAMLLoader

from .. import path, views
from .base import BaseApp


class App(BaseApp):

    name = __name__
    prefix = 'POOLDIN'

    views = views.all

    def init_middleware(self):
        self.after_request(self.inject_response_headers)

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
