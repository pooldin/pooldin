from flask import redirect, url_for

from .base import BaseView


class ViewHomeIndex(BaseView):
    name = 'index'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/', view_func=view)

    def get(self):
        return redirect(url_for('campaign_create'))
