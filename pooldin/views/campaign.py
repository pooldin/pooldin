from flask import abort, render_template

from .base import BaseView
from ..app.negotiate import supports
from ..database.models import User


class ViewCampaignCreate(BaseView):
    name = 'campaign_create'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/campaign/new', view_func=view)
        app.add_post_rule('/campaign/new', view_func=view)

    def get(self):
        return render_template('campaign/create.html')

    @supports('application/json', 'application/x-www-form-urlencoded')
    def post(self):
        abort(503)


class ViewCampaignDetails(BaseView):
    name = 'campaign_details'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/campaign/<int:id>', view_func=view)

    def get(self, id):
        organizer = User.query.filter_by(username='kevin').first()
        return render_template('campaign/details.html', organizer=organizer)
