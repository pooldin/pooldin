from flask import abort, render_template

from .base import BaseView
from ..app.negotiate import supports


class ViewCampaignCreate(BaseView):
    name = 'campaign_create'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/campaign/new', view_func=view)
        app.add_post_rule('/campaign/new', view_func=view)

    def get(self):
        return render_template('campaign/new.html')

    @supports('application/json')
    def post(self):
        abort(405)


class ViewCampaignDetails(BaseView):
    name = 'campaign_index'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/campaign/<int:id>', view_func=view)

    def get(self, id):
        return render_template('campaign/details.html')
