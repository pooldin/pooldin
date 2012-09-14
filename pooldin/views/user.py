from flask import render_template, request

from ..app.negotiate import supports
from .base import BaseView
from ..forms import FormUserLogin


class ViewUserLogin(BaseView):
    name = 'user_login'

    @classmethod
    def add_routes(cls, app, view):
        app.add_get_rule('/login', view_func=view)
        app.add_post_rule('/login', view_func=view)

    def get(self):
        return render_template('user/login.html', form=FormUserLogin())

    @supports('application/json', 'application/x-www-form-urlencoded')
    def post(self):
        if request.form:
            data = request.form.to_dict()
        else:
            data = request.json

        form = FormUserLogin(data)

        valid = form.validate()

        if not valid:
            return render_template('user/login.html', form=form)
